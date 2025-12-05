# LabelImg 标注指南

## 📋 类别说明

本项目按**颜色+形状**组合分类，需要标注以下4种积木：
- `green_cube` - 绿色立方体
- `purple_cube` - 紫色立方体
- `blue_cube` - 蓝色立方体
- `yellow_cylinder` - 黄色圆柱体

**注意**：类别名称格式为 `颜色_形状`，必须完全匹配（包括下划线）。

## 🔧 安装 LabelImg

### 方法1: 使用 pip 安装（推荐）
```bash
pip3 install --break-system-packages labelImg setuptools
```

### 方法2: 如果遇到 Python 3.12 兼容性问题

如果遇到 `ModuleNotFoundError: No module named 'distutils'` 错误：
```bash
pip3 install --break-system-packages setuptools
pip3 install --break-system-packages labelImg
```

### 方法3: 使用修复脚本启动（推荐）

如果直接运行 `labelImg` 出错，可以使用项目提供的修复脚本：
```bash
cd /home/student26/ObjectDetection/dataset
python3 fix_labelimg.py
```

## 🚀 启动 LabelImg


cd /home/student26/ObjectDetection/dataset
./start_labeling_train.sh


**推荐方式**：使用项目提供的启动脚本（会自动处理兼容性问题）：
```bash
cd /home/student26/ObjectDetection/dataset
./start_labeling_train.sh  # 标注训练集
# 或
./start_labeling_val.sh    # 标注验证集
```

**直接启动**：
```bash
labelImg
```

⚠️ **注意**：如果直接运行 `labelImg` 出错，请使用修复脚本或启动脚本。

## 📝 标注步骤

### 1. 设置保存格式为 YOLO 格式

启动 LabelImg 后：
1. 点击左侧的 **"YOLO"** 按钮（重要！确保是YOLO格式，不是PascalVOC格式）
2. 或者使用快捷键：`Ctrl + Shift + Y`

### 2. 打开图片文件夹

1. 点击 **"Open Dir"** 按钮
2. 选择对应的图片文件夹：
   - 训练集：`/home/student26/ObjectDetection/dataset/images/train`
   - 验证集：`/home/student26/ObjectDetection/dataset/images/val`

### 3. 设置保存标注文件的位置

1. 点击 **"Change Save Dir"** 按钮
2. 选择对应的标注文件夹：
   - 训练集标注：`/home/student26/ObjectDetection/dataset/lables/train`
   - 验证集标注：`/home/student26/ObjectDetection/dataset/lables/val`

### 4. 加载类别列表（可选但推荐）

1. 点击菜单栏 **"View"** → **"Auto Save"**（自动保存，方便）
2. 点击菜单栏 **"View"** → **"Auto Save Mode"**（可选，自动保存模式）

如果你想预设类别名称：
1. 点击菜单栏 **"Edit"** → **"PascalVOC Label"**（但这主要适用于PascalVOC格式）
2. 或者在标注时直接输入类别名称

### 5. 开始标注

**快捷键：**
- `W` - 创建边界框
- `D` - 下一张图片
- `A` - 上一张图片
- `Ctrl + S` - 保存当前标注
- `Del` - 删除选中的边界框

**标注流程：**
1. 按 `W` 键开始画框
2. 在图片上按住鼠标左键，拖动画出包围物体的矩形框
3. 松开鼠标后，会弹出类别选择窗口
4. 输入类别名称（如：`green_cube`、`purple_cube`、`blue_cube`、`yellow_cylinder`）
5. 按 `D` 键跳到下一张图片，LabelImg 会自动保存当前标注
6. 重复以上步骤标注所有图片

### 6. 验证标注文件

标注完成后，每个图片会生成对应的 `.txt` 文件，格式如下：

```
0 0.5 0.5 0.2 0.3
1 0.7 0.3 0.15 0.2
```

格式说明：`class_id center_x center_y width height`（所有值都是相对于图片大小的比例，0-1之间）

## 📁 数据集结构

```
dataset/
├── images/
│   ├── train/          # 训练图片
│   └── val/            # 验证图片
├── lables/             # 注意：这里是 lables（拼写问题）
│   ├── train/          # 训练标注文件（.txt格式）
│   └── val/            # 验证标注文件（.txt格式）
└── classes.txt         # 类别列表
```

## ✅ 标注完成后检查

1. **检查文件数量**：标注文件数量应该等于图片数量
   ```bash
   # 检查训练集
   ls dataset/images/train/*.png | wc -l
   ls dataset/lables/train/*.txt | wc -l
   
   # 检查验证集
   ls dataset/images/val/*.png | wc -l
   ls dataset/lables/val/*.txt | wc -l
   ```

2. **检查标注文件格式**：打开一个 `.txt` 文件，确保格式正确

3. **类别编号对应关系**：
   - 0: green_cube
   - 1: purple_cube
   - 2: blue_cube
   - 3: yellow_cylinder

## 💡 提示

1. **确保一致性**：同一类别的积木使用相同的类别名称（注意大小写和拼写）
2. **标注框要紧密**：边界框应该尽可能紧密地包围物体，但不要裁剪物体
3. **标注所有可见物体**：如果一张图片中有多个积木，都要标注
4. **定期保存**：建议启用自动保存功能，避免丢失工作

## 🐛 常见问题

**Q: 运行时出现 `ModuleNotFoundError: No module named 'distutils'` 错误？**  
A: 这是因为 Python 3.12 移除了 distutils。解决方法：
```bash
pip3 install --break-system-packages setuptools
```
然后使用 `./start_labeling_train.sh` 脚本启动，或直接运行 `python3 fix_labelimg.py`。

**Q: 运行时出现 `TypeError: expected str, bytes or os.PathLike object, not NoneType` 错误？**  
A: 这个错误通常发生在没有先打开图片文件夹就进行操作。解决步骤：
1. 启动 labelImg 后，**先点击 "Open Dir"** 选择图片文件夹
2. 然后点击 "Change Save Dir" 选择保存位置
3. 不要在没有打开图片的情况下尝试其他操作

**Q: 标注文件保存在哪里？**  
A: 确保在标注前设置了 "Change Save Dir"，标注文件会保存在你指定的文件夹中。

**Q: 如何批量修改类别名称？**  
A: LabelImg不支持批量修改，但可以在标注时使用快捷键输入类别名称，保持一致性。

**Q: 如何知道标注是否正确？**  
A: 可以使用YOLO训练脚本来验证数据集，或者使用可视化工具查看标注结果。

