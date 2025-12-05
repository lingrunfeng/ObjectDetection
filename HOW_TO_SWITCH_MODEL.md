# 🔧 如何切换模型

## 📝 简单方法

打开文件：`src/yolov8_ros2/launch/camera_yolo.launch.py`

在文件顶部，你会看到：

```python
# ============================================================================
# 🔧 模型配置 - 在这里修改要使用的模型
# ============================================================================
# 默认使用 COCO 模型（识别很多物体：person, laptop, bed, tv 等）
MODEL_PATH = "yolov8n.pt"

# 如果需要使用自定义积木模型，取消下面的注释，注释掉上面的：
# MODEL_PATH = "/home/student26/ObjectDetection/blocks_yolov8n.pt"
# ============================================================================
```

## 🚀 使用方法

### 默认（COCO 模型）- 识别很多物体

文件已经设置好了，直接启动：
```bash
ros2 launch yolov8_ros2 camera_yolo.launch.py
```

### 切换到积木模型

编辑 `src/yolov8_ros2/launch/camera_yolo.launch.py`，找到 `MODEL_PATH` 这一行：

**改成这样：**
```python
# MODEL_PATH = "yolov8n.pt"  # 注释掉这行
MODEL_PATH = "/home/student26/ObjectDetection/blocks_yolov8n.pt"  # 取消注释这行
```

然后重新构建并启动：
```bash
cd /home/student26/ObjectDetection
colcon build --symlink-install --packages-select yolov8_ros2
source install/setup.bash
ros2 launch yolov8_ros2 camera_yolo.launch.py
```

## 📋 可用的模型

1. **COCO 模型**（默认）
   - `MODEL_PATH = "yolov8n.pt"`
   - 识别：person, laptop, bed, tv, bowl, car, dog, cat 等80种物体

2. **积木模型**
   - `MODEL_PATH = "/home/student26/ObjectDetection/blocks_yolov8n.pt"`
   - 识别：red_rectangle, red_triangle, red_cube, blue_cube

3. **其他模型**
   - `MODEL_PATH = "/path/to/your/model.pt"`
   - 替换为你的模型路径

## 💡 提示

- **只需修改一个变量**：`MODEL_PATH`
- **修改后重新构建**：`colcon build --symlink-install --packages-select yolov8_ros2`
- **位置在文件顶部**：很容易找到

就这么简单！🎉








