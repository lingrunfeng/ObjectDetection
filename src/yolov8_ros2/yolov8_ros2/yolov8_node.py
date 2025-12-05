# Basic ROS2
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rclpy.qos import ReliabilityPolicy, QoSProfile

# Executor and callback imports
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor

# ROS2 interfaces
from sensor_msgs.msg import Image, CameraInfo
from std_msgs.msg import String

# Image msg parser
from cv_bridge import CvBridge
import cv2

# Vision model
from ultralytics import YOLO

# Others
import numpy as np
import time, json, torch
import os

class Yolov8Node(Node):
    
    def __init__(self):
        super().__init__("yolov8_node")
        rclpy.logging.set_logger_level('yolov8_node', rclpy.logging.LoggingSeverity.INFO)
        
        ## 🚀 参数设置
        # 默认使用 yolov8n.pt，如果启用 OpenVINO 将自动导出/加载
        self.declare_parameter("model", "yolov8n.pt") 
        self.model_name = self.get_parameter("model").get_parameter_value().string_value
        
        self.declare_parameter("device", "cpu")
        self.device = self.get_parameter("device").get_parameter_value().string_value
        
        self.declare_parameter("threshold", 0.5)
        self.threshold = self.get_parameter("threshold").get_parameter_value().double_value
        
        self.declare_parameter("enable_yolo", True)
        self.enable_yolo = self.get_parameter("enable_yolo").get_parameter_value().bool_value

        # OpenVINO 加速开关
        self.declare_parameter("use_openvino", True)
        self.use_openvino = self.get_parameter("use_openvino").get_parameter_value().bool_value

        ## 初始化
        self.group_1 = MutuallyExclusiveCallbackGroup() # 订阅回调
        self.group_2 = MutuallyExclusiveCallbackGroup() # 处理回调
        
        self.cv_bridge = CvBridge()
        
        # 模型加载逻辑
        if self.use_openvino:
            self.get_logger().info("🚀 OpenVINO acceleration enabled!")
            self.load_openvino_model()
        else:
            self.get_logger().info(f"Loading YOLO model: {self.model_name} on {self.device}...")
            self.yolo = YOLO(self.model_name)
            # Log model classes to verify it's the correct model
            if hasattr(self.yolo, 'model') and hasattr(self.yolo.model, 'names'):
                classes = list(self.yolo.model.names.values())[:10]
                self.get_logger().info(f"✅ Model loaded! Classes: {classes}")
            self.get_logger().info("YOLO model loaded!")
        
        self.color_image_msg = None
        
        # Publishers
        self._item_dict_pub = self.create_publisher(String, "/yolo/prediction/item_dict", 10)
        self._pred_pub = self.create_publisher(Image, "/yolo/prediction/image", 10)
        
        # Subscribers
        self._color_image_sub = self.create_subscription(Image, "/camera/camera/color/image_raw", self.color_image_callback, qos_profile_sensor_data, callback_group=self.group_1)
        
        # Timers - 极限高频
        self._vision_timer = self.create_timer(0.02, self.object_detection, callback_group=self.group_2) # 50 Hz target

    def load_openvino_model(self):
        # 检查是否已经有导出的模型
        base_name = self.model_name.replace('.pt', '')
        ov_model_path = f"{base_name}_openvino_model/"
        
        if os.path.exists(ov_model_path):
            self.get_logger().info(f"Found existing OpenVINO model: {ov_model_path}")
            self.yolo = YOLO(ov_model_path)
        else:
            self.get_logger().info(f"Exporting {self.model_name} to OpenVINO format... This may take a while.")
            try:
                # 加载 PyTorch 模型
                model = YOLO(self.model_name)
                # 导出为 OpenVINO
                model.export(format="openvino")
                # 加载导出的模型
                self.yolo = YOLO(ov_model_path)
                self.get_logger().info("✅ OpenVINO export and load successful!")
            except Exception as e:
                self.get_logger().error(f"OpenVINO export failed: {e}. Falling back to standard PyTorch model.")
                self.yolo = YOLO(self.model_name)

    def color_image_callback(self, msg):
        self.color_image_msg = msg

    def object_detection(self):
        if self.enable_yolo and self.color_image_msg is not None:
            start_time = time.time()
            
            try:
                # 1. 转换图像
                cv_image = self.cv_bridge.imgmsg_to_cv2(self.color_image_msg, desired_encoding='bgr8')
            except Exception as e:
                self.get_logger().error(f"Image conversion error: {e}")
                return

            # 2. 推理 (OpenVINO会自动使用)
            # task='detect' 确保只进行检测
            results = self.yolo.predict(
                source=cv_image,
                verbose=False,
                stream=False,
                conf=self.threshold,
                device=self.device,
                task='detect' 
            )
            
            # 3. 结果处理
            result = results[0]
            annotated_frame = result.plot()
            
            # 4. 发布图像
            try:
                img_msg = self.cv_bridge.cv2_to_imgmsg(annotated_frame, encoding="bgr8")
                img_msg.header = self.color_image_msg.header
                self._pred_pub.publish(img_msg)
            except Exception as e:
                self.get_logger().error(f"Image publish error: {e}")

            # 5. 数据发布
            item_dict = {}
            if len(result.boxes) > 0:
                boxes = result.boxes
                classes = boxes.cls.cpu().numpy().astype(int)
                names = result.names
                xywh = boxes.xywh.cpu().numpy()
                
                detected_items = []
                for i, (cls_id, box) in enumerate(zip(classes, xywh)):
                    item_name = names[cls_id]
                    detected_items.append(item_name)
                    item_dict[f'item_{i}'] = {
                        'class': item_name,
                        'center_2d': [float(box[0]), float(box[1])]
                    }
                
                fps = 1.0 / (time.time() - start_time)
                self.get_logger().info(f"🚀 FPS: {fps:.1f} | Detected: {detected_items}")
            
            msg = String()
            msg.data = json.dumps(item_dict)
            self._item_dict_pub.publish(msg)
            
    def shutdown_callback(self):
        self.get_logger().warn("Shutting down...")

def main(args=None):
    rclpy.init(args=args)
    vision_node = Yolov8Node()
    executor = MultiThreadedExecutor()
    executor.add_node(vision_node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        vision_node.shutdown_callback()
        executor.shutdown()
        vision_node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
