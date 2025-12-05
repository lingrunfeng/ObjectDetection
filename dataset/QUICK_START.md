# 🚀 快速开始标注

## ✅ 环境已就绪

- ✅ labelme 已安装并修复兼容性问题
- ✅ Python 3.12.3 (Ubuntu 24.04)
- ✅ NumPy 兼容性问题已解决
- ✅ 训练集: 14 张图片
- ✅ 验证集: 5 张图片

## 📝 开始标注

### 第一步：标注训练集

```bash
cd /home/student26/ObjectDetection/dataset
./start_labelme_train.sh
```

**标注操作：**
1. 按 `W` 键创建矩形框
2. 在图片上拖动画框，包围积木
3. 输入类别名称（见下方类别列表）
4. 按 `Ctrl+S` 保存，或自动保存
5. 关闭窗口继续下一张图片

### 第二步：标注验证集

```bash
cd /home/student26/ObjectDetection/dataset
./start_labelme_val.sh
```

使用相同的标注方法。

### 第三步：转换为 YOLO 格式

标注完成后，labelme 会生成 JSON 文件，需要转换为 YOLO 格式的 TXT 文件：

```bash
# 转换训练集
python3 labelme_to_yolo.py lables/train lables/train images/train

# 转换验证集
python3 labelme_to_yolo.py lables/val lables/val images/val
```

### 第四步：验证标注

```bash
./check_labels.sh
```

应该看到所有图片都有对应的标注文件。

## 📋 类别列表

标注时，使用以下类别名称（必须完全一致）：

- `green_cube` - 绿色立方体
- `purple_cube` - 紫色立方体
- `blue_cube` - 蓝色立方体
- `yellow_cylinder` - 黄色圆柱体

**注意**：类别名称格式为 `颜色_形状`，必须完全匹配（包括下划线）。

## 🎯 Labelme 快捷键

- `W` - 创建矩形框
- `A` - 上一张图片
- `D` - 下一张图片
- `Del` - 删除选中的标注框
- `Ctrl+S` - 保存标注
- `Ctrl+D` - 复制标注框

## ✅ 验证环境

如果不确定环境是否正常，可以运行测试脚本：

```bash
./test_labelme.sh
```

## 🔧 如果遇到问题

1. **labelme 无法启动**：运行 `./test_labelme.sh` 检查环境
2. **转换失败**：确保安装了 Pillow：`pip3 install --break-system-packages Pillow`
3. **其他问题**：查看 `ALTERNATIVE_LABELING.md` 或 `TROUBLESHOOTING.md`

## 📊 标注进度

- 训练集：14 张图片需要标注
- 验证集：5 张图片需要标注
- 总计：19 张图片

标注完成后，就可以开始训练 YOLO 模型了！






