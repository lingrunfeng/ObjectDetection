## 环境已配置完成

### 已完成的工作

1. 修复 labelme 的 NumPy 兼容性问题

* 问题：NumPy 1.26+ 移除了 np.bool
* 修复：已将 np.bool 替换为 np.bool_
* 结果：labelme 可正常导入和运行

1. 验证环境

* Python 3.12.3 (Ubuntu 24.04)
* labelme 5.9.1
* Pillow 10.2.0
* NumPy 1.26.4
* 训练集：14 张图片
* 验证集：5 张图片

### 现在可以直接开始标注

标注训练集（14张图片）：

**cd** **/home/student26/ObjectDetection/dataset**

**./start_labelme_train.sh**

标注验证集（5张图片）：

**cd** **/home/student26/ObjectDetection/dataset**

**./start_labelme_val.sh**

### 标注完成后


转换标注为 YOLO 格式：

**# 转换训练集**

**python3** **labelme_to_yolo.py** **lables/train** **lables/train** **images/train**

**# 转换验证集  **

**python3** **labelme_to_yolo.py** **lables/val** **lables/val** **images/val**

### 验证环境

如果不确定，运行测试：

**cd** **/home/student26/ObjectDetection/dataset**

**./test_labelme.sh**

### 标注时使用的类别

* red_rectangle
* red_triangle
* red_cube
* blue_cube

可以开始标注。所有环境已配置好，labelme 可直接使用。如有问题，告诉我。


## 开始训练

### 方法1：直接训练（推荐）

**cd** **/home/student26/ObjectDetection/dataset**

**python3** **train_yolo.py**

### 方法2：使用快速脚本

**cd** **/home/student26/ObjectDetection/dataset**

**./start_training.sh**

训练过程：* 自动显示进度

* 实时显示 Loss 和 mAP 指标
* 自动保存最佳模型
* 训练结果保存在 runs/detect/train/

预计训练时间：* CPU: 约 1-2 小时

* GPU: 约 10-30 分钟

---

## 验证训练结果

训练完成后，运行：

**cd** **/home/student26/ObjectDetection/dataset**

**python3** **validate_training.py**

这会：1. 自动找到训练好的最佳模型

1. 在验证集上测试性能
2. 显示 mAP50 和 mAP50-95 指标
2. 

1. 显示每个类别的性能
2. 在测试图片上生成检测结果

### 预期输出示例：

**📊 验证结果:**

**  mAP50: 0.xxxx**

**  mAP50-95: 0.xxxx**

**📋 各类别性能:**

**  red_rectangle: mAP50=0.xxxx, mAP50-95=0.xxxx**

**  red_triangle: mAP50=0.xxxx, mAP50-95=0.xxxx**

**  ...**

### 如何判断模型质量：

* 优秀: mAP50 > 0.9
* 良好: mAP50 > 0.8
* 可用: mAP50 > 0.7
* 需要改进: mAP50 < 0.7

---

## 其他验证方法

### 查看训练曲线图：

**cd** **/home/student26/ObjectDetection/dataset**

**ls** **runs/detect/train/*****.png**

查看 results.png 可以看到：* Loss 曲线（应该下降）

* mAP 曲线（应该上升）
* Precision/Recall 曲线

### 查看最佳模型：


