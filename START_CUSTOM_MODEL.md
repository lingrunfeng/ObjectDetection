# 🚀 启动自定义训练模型

## ✅ 模型已准备

训练好的模型已复制到项目根目录：
- `blocks_yolov8n.pt` - 你的自定义积木检测模型

## 🎯 启动步骤

### 第一步：设置环境

```bash
cd /home/student26/ObjectDetection
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

### 第二步：启动相机 + YOLO 节点

```bash
ros2 launch yolov8_ros2 camera_yolo.launch.py
```

**Launch文件已自动配置为使用你的自定义模型！**

### 第三步：在另一个终端打开 Rviz2

```bash
cd /home/student26/ObjectDetection
source /opt/ros/jazzy/setup.bash
source install/setup.bash
rviz2
```

### 第四步：在 Rviz2 中配置

1. **设置 Fixed Frame**:
   - 在左侧面板找到 "Global Options"
   - 将 "Fixed Frame" 改为 `camera_link`

2. **添加图像显示**:
   - 点击左下角 "Add" 按钮
   - 选择 "Image" 类型
   - 点击 "OK"
   - 在 "Image" 面板中，设置 "Image Topic" 为: `/yolo/prediction/image`
   - 现在应该能看到带检测框的图像，显示检测到的积木！

3. **（可选）添加原始相机图像**:
   - 再次点击 "Add" → "Image"
   - 设置 "Image Topic" 为: `/camera/camera/color/image_raw`

## 📡 查看检测结果

### 方法1: Rviz2（推荐）
- 可以看到实时检测结果，带检测框和标签

### 方法2: 查看检测数据
```bash
# 查看检测到的物体信息
ros2 topic echo /yolo/prediction/item_dict
```

### 方法3: 使用 rqt_image_view（简单快速）
```bash
rqt_image_view
```
然后在下拉菜单中选择话题：`/yolo/prediction/image`

## 🔍 验证模型是否在工作

### 检查话题：
```bash
ros2 topic list | grep yolo
```

应该看到：
- `/yolo/prediction/image` - 检测结果图像
- `/yolo/prediction/item_dict` - 检测结果数据

### 查看检测日志：
在启动 YOLO 的终端中，应该看到类似：
```
🚀 FPS: XX.X | Detected: ['red_rectangle', 'blue_cube', ...]
```

## 🎯 检测的类别

你的模型可以检测以下4种积木：
- `red_rectangle` - 红色长方形积木
- `red_triangle` - 红色三角形积木
- `red_cube` - 红色立方体积木
- `blue_cube` - 蓝色立方体积木

## ⚙️ 调整检测阈值（可选）

如果检测不到物体或检测太多误报，可以调整阈值：

```bash
ros2 launch yolov8_ros2 camera_yolo.launch.py threshold:=0.3
```

阈值范围：0.0 - 1.0
- 更低（如 0.3）：检测更多物体，但可能有误报
- 更高（如 0.7）：只检测很确信的物体，但可能漏检

## 🔧 手动指定模型路径

如果需要使用不同的模型：

```bash
ros2 launch yolov8_ros2 camera_yolo.launch.py model:=/path/to/your/model.pt
```

## 🐛 故障排除

### 1. 看不到检测结果
- 确保相机正对积木
- 检查光照条件
- 查看终端日志，看是否有错误

### 2. 模型加载失败
- 检查模型文件是否存在：`ls -lh blocks_yolov8n.pt`
- 检查文件路径是否正确

### 3. 相机未检测到
- 检查相机连接：`lsusb | grep Intel`
- 确保相机在USB 3.0端口

## 💡 提示

- 确保积木在相机视野中，且光线充足
- 检测框会显示在 Rviz2 的图像上
- 可以在控制台看到检测到的物体列表和FPS

祝你测试顺利！🎉








