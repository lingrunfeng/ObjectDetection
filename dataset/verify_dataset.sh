#!/bin/bash

# 数据集验证脚本 - 一键验证所有标注

echo "============================================================"
echo "🔍 数据集完整验证"
echo "============================================================"
echo ""

cd "$(dirname "$0")"

# 1. 基本文件检查
echo "1️⃣  检查文件完整性..."
echo ""
python3 check_labels.sh 2>&1 | grep -A 10 "数据集统计"

# 2. 标注质量验证
echo ""
echo "2️⃣  验证标注质量..."
echo ""
python3 validate_annotations.py 2>&1 | grep -A 30 "验证结果"

# 3. 显示统计摘要
echo ""
echo "============================================================"
echo "📊 数据集摘要"
echo "============================================================"

TRAIN_IMGS=$(ls images/train/*.png 2>/dev/null | wc -l)
VAL_IMGS=$(ls images/val/*.png 2>/dev/null | wc -l)
TRAIN_LABELS=$(ls lables/train/*.txt 2>/dev/null | wc -l)
VAL_LABELS=$(ls lables/val/*.txt 2>/dev/null | wc -l)

TRAIN_ANNOTATIONS=$(find lables/train -name "*.txt" -exec cat {} \; 2>/dev/null | wc -l)
VAL_ANNOTATIONS=$(find lables/val -name "*.txt" -exec cat {} \; 2>/dev/null | wc -l)

echo ""
echo "📁 文件统计:"
echo "   训练集: $TRAIN_IMGS 张图片, $TRAIN_LABELS 个标注文件, $TRAIN_ANNOTATIONS 个标注框"
echo "   验证集: $VAL_IMGS 张图片, $VAL_LABELS 个标注文件, $VAL_ANNOTATIONS 个标注框"
echo ""

# 4. 类别统计
echo "📋 类别分布:"
python3 validate_annotations.py 2>&1 | grep -A 10 "类别统计" | tail -10

echo ""
echo "============================================================"
echo "✅ 验证完成！"
echo "============================================================"
echo ""
echo "💡 提示:"
echo "   - 如果所有检查都通过，可以开始训练模型了"
echo "   - 如果发现错误，请根据上面的提示修复"
echo "   - 查看详细验证结果运行: python3 validate_annotations.py"
echo ""








