
import os
import torch
torch_device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


from ament_index_python import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

# ============================================================================
# 🔧 模型配置 - 在这里修改要使用的模型
# ============================================================================
# 默认使用 COCO 模型（识别很多物体：person, laptop, bed, tv 等）,
#cd /home/student26/ObjectDetection
#source install/setup.bash
#ros2 launch yolov8_ros2 camera_yolo.launch.py
# MODEL_PATH = "yolov8n.pt"，/home/student26/ObjectDetection/blocks_yolov8n.pt

# 使用自定义积木模型（训练好的模型）
MODEL_PATH = "/home/student26/ObjectDetection/dataset/runs/detect/blocks_detection/weights/best.pt"

# 如果需要使用其他模型，修改为你的模型路径：
# MODEL_PATH = "yolov8n.pt"  # COCO预训练模型
# ============================================================================

def generate_launch_description():
    this_package_name='yolov8_ros2'
    realsense_package_name = 'realsense2_camera'
    

    # Launch Realsense camera launch file with aligned depth images publisher
    rs_camera = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(realsense_package_name), 'launch', 'rs_launch.py'
        )]), launch_arguments={'align_depth.enable': 'true'}.items()
    )
    
    
    # Run the yolov8 node, with the set device
    # Allow model to be overridden via launch argument, but use MODEL_PATH as default
    from launch.actions import DeclareLaunchArgument
    from launch.substitutions import LaunchConfiguration
    
    # Declare launch argument for model selection (can override MODEL_PATH variable)
    model_arg = DeclareLaunchArgument(
        'model',
        default_value=MODEL_PATH,
        description='Path to YOLO model file. Can override MODEL_PATH variable in this file.'
    )
    
    # Get model path from launch argument
    model_path = LaunchConfiguration('model')
    
    print(f"[Launch] 🔧 Using model: {MODEL_PATH}")
    print(f"[Launch] 💡 Tip: To change model, edit MODEL_PATH variable at top of this file")
    
    yolov8_node = Node(
        package=this_package_name,
        executable='yolov8_node',
        #name='node2', # Default is name of executable
        output='screen',
        parameters=[
            {'device': f'{torch_device}'},
            {'model': model_path},
            {'use_openvino': False},  # Disable OpenVINO for custom model
        ],
    )
    

    # Launch them all!
    return LaunchDescription([
        model_arg,  # Declare the argument first
        rs_camera,
        yolov8_node,
    ])
