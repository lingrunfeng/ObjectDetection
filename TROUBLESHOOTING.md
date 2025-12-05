# 故障排除指南

## ✅ NumPy版本问题已修复

### 问题
YOLOv8节点无法启动，因为NumPy版本不兼容。`cv_bridge`模块是用NumPy 1.x编译的，但系统安装了NumPy 2.2.6。

### 解决方案
已降级NumPy到1.26.4版本：
```bash
pip3 install --break-system-packages "numpy<2" --force-reinstall
```

### 注意
如果遇到opencv-python相关警告，可以尝试：
```bash
pip3 install --break-system-packages "opencv-python<4.13"
```

## 🔄 现在请重新启动

1. **关闭当前的launch文件**（如果还在运行，按Ctrl+C）

2. **重新启动**：
   ```bash
   cd /home/student26/ObjectDetection
   source /opt/ros/jazzy/setup.bash
   source install/setup.bash
   ros2 launch yolov8_ros2 camera_yolo.launch.py
   ```

3. **在另一个终端验证节点是否运行**：
   ```bash
   source /opt/ros/jazzy/setup.bash
   source /home/student26/ObjectDetection/install/setup.bash
   ros2 node list
   ```
   应该看到 `/yolov8_node`

4. **检查话题**：
   ```bash
   ros2 topic list | grep yolo
   ```
   应该看到：
   - `/yolo/prediction/image`
   - `/yolo/prediction/item_dict`

5. **在Rviz2中查看**：
   - 添加Image显示
   - 选择话题：`/yolo/prediction/image`




