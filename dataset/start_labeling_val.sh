#!/bin/bash

# 启动 LabelImg 标注验证集

echo "🚀 启动 LabelImg 标注验证集..."
echo ""
echo "📁 图片目录: $(pwd)/images/val"
echo "📁 标注保存目录: $(pwd)/lables/val"
echo ""
echo "⚠️  重要提示："
echo "1. 启动后，点击左侧 'YOLO' 按钮（确保使用YOLO格式）"
echo "2. 点击 'Open Dir'，选择: $(pwd)/images/val"
echo "3. 点击 'Change Save Dir'，选择: $(pwd)/lables/val"
echo "4. 按 'W' 键开始画框标注"
echo ""
echo "📋 类别列表："
echo "   - red_rectangle"
echo "   - red_triangle"
echo "   - red_cube"
echo "   - blue_cube"
echo ""
echo "按回车键启动 LabelImg..."
read

# 检查 labelImg 是否安装
if ! command -v labelImg &> /dev/null; then
    echo "❌ 错误: labelImg 未安装"
    echo ""
    echo "请先安装 labelImg:"
    echo "  pip3 install --break-system-packages labelImg"
    exit 1
fi

# 尝试启动 labelImg
# 如果 labelImg 命令失败，使用修复脚本
if ! labelImg 2>/dev/null; then
    echo ""
    echo "尝试使用修复脚本启动..."
    python3 "$(dirname "$0")/fix_labelimg.py"
fi

