# 🚀 启动最佳模型并查看检测结果

## ✅ 模型已更新

最佳训练模型已配置：
- 模型路径：`/home/student26/ObjectDetection/dataset/runs/detect/blocks_detection/weights/best.pt`
- 可识别类别：green_cube, purple_cube, blue_cube, yellow_cylinder, red_cube

## 📋 启动步骤

### 第一步：设置环境（在第一个终端）

```bash
cd /home/student26/ObjectDetection
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

### 第二步：启动 YOLO 检测节点（在第一个终端）

```bash
ros2 launch yolov8_ros2 camera_yolo.launch.py
```

**这会启动：**
- 相机节点（Realsense 或 USB 摄像头）
- YOLO 检测节点（使用你的最佳训练模型）

**等待看到类似输出：**
```
[Launch] 🔧 Using model: /home/student26/ObjectDetection/dataset/runs/detect/blocks_detection/weights/best.pt
🚀 YOLO Node started
```

### 第三步：启动 Rviz2 查看结果（在第二个终端）

```bash
cd /home/student26/ObjectDetection
source /opt/ros/jazzy/setup.bash
source install/setup.bash
rviz2
```

### 第四步：在 Rviz2 中配置显示

1. **设置 Fixed Frame**：
   - 在左侧面板找到 "Global Options"
   - 将 "Fixed Frame" 从 `map` 改为 `camera_link`（或 `camera_color_optical_frame`）

2. **添加检测结果图像显示**：
   - 点击左下角 "Add" 按钮
   - 选择 "Image" 类型
   - 点击 "OK"
   - 在 "Image" 面板中，设置 "Image Topic" 为：`/yolo/prediction/image`
   - ✅ 现在应该能看到带检测框的图像，显示检测到的积木！

3. **（可选）添加原始相机图像**：
   - 再次点击 "Add" → "Image"
   - 设置 "Image Topic" 为：`/camera/color/image_raw`（Realsense）或 `/camera/image_raw`（USB摄像头）

4. **（可选）保存配置**：
   - 点击 "File" → "Save Config As"
   - 保存为 `yolo_detection.rviz`，下次可以直接加载

## 🎯 应该看到什么

在 `/yolo/prediction/image` 话题中：
- ✅ 彩色图像，带有：
  - YOLO 检测框（边界框）
  - 类别标签（green_cube, purple_cube, blue_cube, yellow_cylinder, red_cube）
  - 置信度分数

## 🔍 验证检测是否工作

### 方法1：检查话题列表

```bash
ros2 topic list | grep yolo
```

应该看到：
- `/yolo/prediction/image` - 检测结果图像
- `/yolo/prediction/item_dict` - 检测结果数据（JSON格式）

### 方法2：查看检测数据

```bash
ros2 topic echo /yolo/prediction/item_dict
```

会显示检测到的物体信息，包括类别和位置。

### 方法3：使用 rqt_image_view（简单快速）

如果不想用 Rviz2，可以用更简单的工具：

```bash
rqt_image_view
```

然后在下拉菜单中选择话题：`/yolo/prediction/image`

## 🎨 检测的类别

你的模型可以检测以下5种积木：
- 🟢 `green_cube` - 绿色立方体
- 🟣 `purple_cube` - 紫色立方体
- 🔵 `blue_cube` - 蓝色立方体
- 🟡 `yellow_cylinder` - 黄色圆柱体
- 🔴 `red_cube` - 红色立方体

## ⚠️ 如果遇到问题

### 问题1：找不到相机话题

检查相机是否正常发布图像：
```bash
ros2 topic list | grep camera
ros2 topic echo /camera/color/image_raw --once
```

### 问题2：Rviz2 中看不到图像

- 确认 Fixed Frame 设置正确
- 检查话题名称是否正确：`/yolo/prediction/image`
- 在 Rviz2 中点击 "Reset" 按钮

### 问题3：模型加载失败

检查模型文件是否存在：
```bash
ls -lh /home/student26/ObjectDetection/dataset/runs/detect/blocks_detection/weights/best.pt
```

### 问题4：使用 USB 摄像头

如果使用 USB 摄像头而不是 Realsense，可能需要：
1. 安装 USB 摄像头驱动
2. 修改 launch 文件中的相机配置
3. 或使用其他相机节点发布图像到 `/camera/color/image_raw` 话题

## 💡 提示

- **保存 Rviz2 配置**：配置好后保存，下次直接加载
- **调整检测阈值**：可以在 launch 文件中修改 `threshold` 参数（默认 0.5）
- **查看日志**：在启动 YOLO 的终端中可以看到检测日志和 FPS

---

**现在可以开始测试你的模型了！** 🎉

