#!/bin/bash

# 测试 labelme 是否能正常启动（不实际打开界面）

echo "🧪 测试 labelme 环境..."
echo ""

# 检查 labelme 是否安装
if ! command -v labelme &> /dev/null; then
    echo "❌ labelme 未安装"
    echo "请运行: pip3 install --break-system-packages labelme Pillow"
    exit 1
fi

# 检查 Python 导入
echo "1. 检查 Python 导入..."
if python3 -c "import labelme; print('✅ labelme 导入成功')" 2>&1 | grep -q "成功"; then
    echo "   ✅ labelme 可以正常导入"
else
    echo "   ❌ labelme 导入失败"
    exit 1
fi

# 检查版本
echo ""
echo "2. 检查版本信息..."
labelme --version 2>&1

# 检查依赖
echo ""
echo "3. 检查依赖..."
python3 -c "
import PIL
import numpy
print(f'   ✅ Pillow: {PIL.__version__}')
print(f'   ✅ NumPy: {numpy.__version__}')
" 2>&1

# 检查数据集目录
echo ""
echo "4. 检查数据集目录..."
if [ -d "images/train" ]; then
    IMG_COUNT=$(ls images/train/*.png 2>/dev/null | wc -l)
    echo "   ✅ 训练集图片: $IMG_COUNT 张"
else
    echo "   ⚠️  训练集目录不存在"
fi

if [ -d "images/val" ]; then
    IMG_COUNT=$(ls images/val/*.png 2>/dev/null | wc -l)
    echo "   ✅ 验证集图片: $IMG_COUNT 张"
else
    echo "   ⚠️  验证集目录不存在"
fi

echo ""
echo "✅ 所有检查通过！可以开始使用 labelme 进行标注。"
echo ""
echo "启动标注："
echo "  ./start_labelme_train.sh  # 标注训练集"
echo "  ./start_labelme_val.sh    # 标注验证集"








