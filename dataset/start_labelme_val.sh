#!/bin/bash

# 启动 Labelme 标注验证集

echo "🚀 启动 Labelme 标注验证集..."
echo ""
echo "📁 图片目录: $(pwd)/images/val"
echo "📁 标注保存目录: $(pwd)/lables/val"
echo ""
echo "⚠️  重要提示："
echo "1. Labelme 会自动保存为 JSON 格式"
echo "2. 标注完成后，运行以下命令转换为 YOLO 格式："
echo "   python3 labelme_to_yolo.py lables/val lables/val images/val"
echo ""
echo "📋 类别列表："
echo "   - green_cube      (绿色立方体)"
echo "   - purple_cube     (紫色立方体)"
echo "   - blue_cube       (蓝色立方体)"
echo "   - yellow_cylinder (黄色圆柱体)"
echo ""
echo "📝 使用说明："
echo "   - 按 'W' 键创建矩形框"
echo "   - 画框后输入类别名称"
echo "   - 按 Ctrl+S 保存（或自动保存）"
echo "   - 关闭窗口切换到下一张图片"
echo ""
echo "按回车键启动 Labelme..."
read

# 检查 labelme 是否安装
if ! command -v labelme &> /dev/null; then
    echo "❌ 错误: labelme 未安装"
    echo ""
    echo "请先安装 labelme:"
    echo "  pip3 install --break-system-packages labelme"
    exit 1
fi

# 启动 labelme
cd "$(dirname "$0")"
labelme images/val --output lables/val --nodata






