# 🔄 切换模型指南

## 📦 可用的模型

1. **自定义积木检测模型**（当前默认）
   - 路径: `/home/student26/ObjectDetection/blocks_yolov8n.pt`
   - 类别: red_rectangle, red_triangle, red_cube, blue_cube (4种积木)

2. **默认 COCO 模型**（识别很多类别）
   - 路径: `yolov8n.pt` (会自动下载)
   - 类别: person, laptop, bed, tv, bowl, 等等 (80种常见物体)

## 🚀 切换方法

### 方法1: 通过启动参数切换（推荐）⭐

#### 使用自定义积木模型：
```bash
ros2 launch yolov8_ros2 camera_yolo.launch.py model:=/home/student26/ObjectDetection/blocks_yolov8n.pt
```

#### 使用默认 COCO 模型：
```bash
ros2 launch yolov8_ros2 camera_yolo.launch.py model:=yolov8n.pt
```

### 方法2: 临时修改（快速切换）

编辑 `src/yolov8_ros2/launch/camera_yolo.launch.py` 文件，修改这一行：

```python
# 使用自定义模型
custom_model_path = '/home/student26/ObjectDetection/blocks_yolov8n.pt'

# 或使用默认模型（注释掉上面，取消注释下面）
# custom_model_path = 'yolov8n.pt'
```

然后重新构建：
```bash
cd /home/student26/ObjectDetection
colcon build --symlink-install --packages-select yolov8_ros2
source install/setup.bash
```

## 🎯 快速启动脚本（最简单）⭐

已经为你创建了两个便捷脚本，切换非常方便！

### 使用自定义积木模型：
```bash
cd /home/student26/ObjectDetection
./start_blocks_model.sh
```

### 使用默认 COCO 模型（识别很多物体）：
```bash
cd /home/student26/ObjectDetection
./start_coco_model.sh
```

---

## 📋 模型对比

| 模型 | 类别数 | 能识别什么 | 使用场景 |
|------|--------|-----------|---------|
| **自定义积木模型** | 4 | red_rectangle, red_triangle, red_cube, blue_cube | 专门检测你的积木 |
| **COCO 模型** | 80 | person, laptop, bed, tv, bowl, car, dog, cat... | 通用物体检测 |

---

## 💡 快速参考

**切换到 COCO 模型（识别很多物体）：**
```bash
./start_coco_model.sh
```

**切换回积木模型：**
```bash
./start_blocks_model.sh
```

就这么简单！

