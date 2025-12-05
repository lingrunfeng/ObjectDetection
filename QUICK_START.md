# 🚀 快速启动命令

## 每次使用前（设置环境）

```bash
cd /home/student26/ObjectDetection
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

## 运行YOLOv8 + 相机

```bash
ros2 launch yolov8_ros2 camera_yolo.launch.py
```

## 查看检测结果（在另一个终端）

```bash
# 方法1: 使用rqt_image_view（简单）
rqt_image_view

# 方法2: 使用rviz2（功能全）
rviz2
```

在可视化工具中选择话题：`/yolo/prediction/image`

## 查看检测数据

```bash
ros2 topic echo /yolo/prediction/item_dict
```

## 重新构建（修改代码后）

```bash
cd /home/student26/ObjectDetection
colcon build --symlink-install
source install/setup.bash
```

---
详细说明请查看 `RUN_GUIDE.md`



