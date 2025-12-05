# LabelImg 故障排除指南

## ❌ 错误：ModuleNotFoundError: No module named 'distutils'

**原因**：Python 3.12+ 移除了 distutils 模块，而旧版本的 labelImg 依赖它。

**解决方法**：
```bash
pip3 install --break-system-packages setuptools
```

然后使用修复脚本启动：
```bash
cd /home/student26/ObjectDetection/dataset
python3 fix_labelimg.py
```

或者直接使用项目提供的启动脚本：
```bash
./start_labeling_train.sh
```

---

## ❌ 错误：TypeError: expected str, bytes or os.PathLike object, not NoneType

**原因**：在没有打开图片文件夹的情况下，labelImg 尝试访问文件路径。

**解决方法**：
1. **启动顺序很重要**！按以下顺序操作：
   - 启动 labelImg
   - **先点击 "Open Dir"**，选择图片文件夹
   - **然后点击 "Change Save Dir"**，选择标注保存文件夹
   - 不要在没有打开文件夹的情况下点击其他按钮

2. 如果错误持续，尝试关闭 labelImg 重新启动，并严格按照上述顺序操作。

---

## ❌ 错误：QSocketNotifier: Can only be used with threads started with QThread

**原因**：这是一个警告，通常不影响功能。如果影响了，可能需要设置环境变量。

**解决方法**（通常不需要）：
```bash
export QT_QPA_PLATFORM=xcb
labelImg
```

---

## ❌ LabelImg 启动后界面空白或卡死

**可能原因**：
1. 图形界面问题
2. 权限问题
3. 依赖缺失

**解决方法**：
1. 检查是否安装了 PyQt5：
   ```bash
   python3 -c "import PyQt5; print('PyQt5 OK')"
   ```

2. 如果未安装：
   ```bash
   sudo apt install python3-pyqt5
   # 或
   pip3 install --break-system-packages PyQt5
   ```

3. 尝试使用修复脚本：
   ```bash
   python3 fix_labelimg.py
   ```

---

## ✅ 推荐的启动流程

为了避免错误，建议使用以下标准流程：

1. **使用启动脚本**（最简单）：
   ```bash
   cd /home/student26/ObjectDetection/dataset
   ./start_labeling_train.sh
   ```

2. **在 labelImg 中的操作顺序**：
   - ✅ 点击左侧 **"YOLO"** 按钮（选择格式）
   - ✅ 点击 **"Open Dir"** → 选择图片文件夹
   - ✅ 点击 **"Change Save Dir"** → 选择标注文件夹
   - ✅ 点击菜单 **"View"** → **"Auto Save"**（启用自动保存）
   - ✅ 开始标注（按 `W` 画框）

---

## 🔄 替代方案：使用 labelme

如果 labelImg 持续出现问题，可以考虑使用 **labelme**（另一个标注工具）：

```bash
# 安装 labelme
pip3 install --break-system-packages labelme

# 启动 labelme（支持 YOLO 格式）
labelme --output labelme_json --flags labels.txt
```

但需要注意，labelme 默认输出 JSON 格式，需要转换后才能用于 YOLO 训练。

---

## 📞 获取帮助

如果以上方法都无法解决问题，请：
1. 检查 Python 版本：`python3 --version`
2. 检查已安装的包：`pip3 list | grep -i label`
3. 查看完整错误信息并记录


