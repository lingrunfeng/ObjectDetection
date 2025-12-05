#!/bin/bash

# 启动使用默认 COCO 模型的节点（识别很多物体）

echo "🚀 启动 YOLO 节点 - 使用默认 COCO 模型（识别很多物体）"
echo ""
echo "这个模型可以识别：person, laptop, bed, tv, bowl, 等等80种常见物体"
echo ""

cd /home/student26/ObjectDetection
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 launch yolov8_ros2 camera_yolo.launch.py model:=yolov8n.pt








