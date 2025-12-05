#!/bin/bash

# 启动使用自定义积木检测模型的节点

echo "🚀 启动 YOLO 节点 - 使用自定义积木检测模型"
echo ""
echo "这个模型可以识别：red_rectangle, red_triangle, red_cube, blue_cube"
echo ""

cd /home/student26/ObjectDetection
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 launch yolov8_ros2 camera_yolo.launch.py model:=/home/student26/ObjectDetection/blocks_yolov8n.pt








