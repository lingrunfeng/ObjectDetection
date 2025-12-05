# 🚀 YOLO 模型训练指南

## 📋 前提条件

✅ 数据集已准备完成（已完成）
- 训练集：14 张图片，56 个标注框
- 验证集：5 张图片，21 个标注框
- 4 个类别：red_rectangle, red_triangle, red_cube, blue_cube

## 🎯 快速开始

### 第一步：验证数据集

在开始训练前，确保数据集正确：

```bash
cd /home/student26/ObjectDetection/dataset
./verify_dataset.sh
```

应该看到：
- ✅ 所有标注文件格式正确
- ✅ 没有错误或警告

### 第二步：开始训练

```bash
cd /home/student26/ObjectDetection/dataset
python3 train_yolo.py
```

**训练参数说明：**
- **模型**: YOLOv8n (nano - 最快最小)
- **训练轮数**: 100 epochs
- **图片大小**: 640x640
- **批次大小**: 16 (可根据GPU内存调整)

**训练时间：**
- CPU: 约 1-2 小时（取决于CPU性能）
- GPU: 约 10-30 分钟

**训练过程中的输出：**
- 实时显示训练进度
- Loss 曲线
- mAP (平均精度)

### 第三步：验证训练结果

训练完成后，验证模型性能：

```bash
python3 validate_training.py
```

这会：
- 在验证集上测试模型
- 显示 mAP 指标
- 显示各类别性能
- 在测试图片上生成检测结果

## 📊 训练结果位置

训练结果保存在：

```
dataset/
└── runs/
    └── detect/
        └── train/
            ├── weights/
            │   ├── best.pt    # 最佳模型（推荐使用）
            │   └── last.pt    # 最后一轮模型
            ├── results.png    # 训练曲线图
            ├── confusion_matrix.png  # 混淆矩阵
            └── ...
```

## 📈 理解训练指标

### 主要指标：

1. **mAP50**: 平均精度 (IoU=0.5)
   - 越高越好，理想值 > 0.8

2. **mAP50-95**: 平均精度 (IoU=0.5-0.95)
   - 更严格的指标，理想值 > 0.5

3. **Precision**: 精确率
   - 检测到的物体中，正确检测的比例

4. **Recall**: 召回率
   - 所有真实物体中，被正确检测到的比例

### 如何判断模型好坏：

- **优秀**: mAP50 > 0.9, mAP50-95 > 0.7
- **良好**: mAP50 > 0.8, mAP50-95 > 0.6
- **可用**: mAP50 > 0.7, mAP50-95 > 0.5
- **需要改进**: mAP50 < 0.7

## 🔧 调整训练参数

如果需要调整训练参数，编辑 `train_yolo.py`：

```python
results = model.train(
    data=str(DATA_YAML),
    epochs=200,        # 增加训练轮数（更准确但更慢）
    imgsz=640,         # 图片大小（可尝试 416, 640, 1280）
    batch=8,           # 批次大小（如果内存不足，减小这个值）
    lr0=0.01,          # 初始学习率（可尝试 0.001-0.01）
    patience=50,       # 早停耐心值
)
```

### 不同模型大小：

```python
model_size = "n"  # nano - 最快最小（推荐开始用这个）
model_size = "s"  # small - 平衡速度和准确度
model_size = "m"  # medium - 更准确但更慢
model_size = "l"  # large - 高准确度
model_size = "x"  # xlarge - 最高准确度
```

## 🧪 测试训练好的模型

### 方法1：使用验证脚本

```bash
python3 validate_training.py
```

### 方法2：在单张图片上测试

```python
from ultralytics import YOLO

# 加载训练好的模型
model = YOLO('runs/detect/train/weights/best.pt')

# 在图片上检测
results = model.predict('images/val/Screenshot from 2025-11-24 17-48-21.png', save=True)
```

### 方法3：在视频上测试

```python
from ultralytics import YOLO

model = YOLO('runs/detect/train/weights/best.pt')
results = model.predict('video.mp4', save=True)
```

## 🚀 在 ROS2 中使用训练好的模型

训练完成后，将模型复制到项目根目录：

```bash
cd /home/student26/ObjectDetection
cp dataset/runs/detect/train/weights/best.pt ./blocks_yolov8n.pt
```

然后在 launch 文件中使用：

```python
ros2 launch yolov8_ros2 camera_yolo.launch.py model:=blocks_yolov8n.pt
```

## 💡 训练技巧

1. **数据增强**: YOLO 默认启用数据增强，提高泛化能力
2. **早停机制**: 如果 50 轮没有改善，自动停止（避免过拟合）
3. **学习率调整**: 模型会自动调整学习率
4. **多模型对比**: 可以训练多个模型大小，选择最好的

## ⚠️ 常见问题

### 1. 训练很慢
- 使用 GPU 加速（如果有）
- 减小批次大小和图片大小
- 使用更小的模型（yolov8n）

### 2. 内存不足
- 减小批次大小（batch=8 或 4）
- 减小图片大小（imgsz=416）

### 3. 准确率不高
- 增加训练轮数（epochs=200）
- 使用更大的模型（yolov8s 或 yolov8m）
- 检查数据集质量（标注是否正确）

### 4. 过拟合（训练集表现好，验证集表现差）
- 增加数据增强
- 使用更多的训练数据
- 减小模型大小

## 📝 下一步

训练完成后：
1. ✅ 验证模型性能
2. ✅ 测试在真实场景中的表现
3. ✅ 部署到 ROS2 系统
4. ✅ 根据实际使用情况调整

祝训练顺利！🎉








