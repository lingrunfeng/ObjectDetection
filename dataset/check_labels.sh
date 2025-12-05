#!/bin/bash

# 检查标注完整性脚本

echo "🔍 检查数据集标注完整性..."
echo ""

# 数据集根目录
DATASET_DIR="/home/student26/ObjectDetection/dataset"
IMAGES_TRAIN="$DATASET_DIR/images/train"
IMAGES_VAL="$DATASET_DIR/images/val"
LABELS_TRAIN="$DATASET_DIR/lables/train"
LABELS_VAL="$DATASET_DIR/lables/val"

# 统计训练集
TRAIN_IMAGES=$(find "$IMAGES_TRAIN" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) | wc -l)
TRAIN_LABELS=$(find "$LABELS_TRAIN" -type f -name "*.txt" | wc -l)

# 统计验证集
VAL_IMAGES=$(find "$IMAGES_VAL" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) | wc -l)
VAL_LABELS=$(find "$LABELS_VAL" -type f -name "*.txt" | wc -l)

echo "📊 数据集统计："
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "训练集："
echo "  图片数量: $TRAIN_IMAGES"
echo "  标注数量: $TRAIN_LABELS"
if [ "$TRAIN_IMAGES" -eq "$TRAIN_LABELS" ]; then
    echo "  ✅ 训练集标注完整"
else
    echo "  ⚠️  训练集缺少 $((TRAIN_IMAGES - TRAIN_LABELS)) 个标注文件"
fi
echo ""
echo "验证集："
echo "  图片数量: $VAL_IMAGES"
echo "  标注数量: $VAL_LABELS"
if [ "$VAL_IMAGES" -eq "$VAL_LABELS" ]; then
    echo "  ✅ 验证集标注完整"
else
    echo "  ⚠️  验证集缺少 $((VAL_IMAGES - VAL_LABELS)) 个标注文件"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查缺少标注的图片
echo "🔍 检查缺少标注的图片："
echo ""

# 训练集
MISSING_TRAIN=0
find "$IMAGES_TRAIN" -maxdepth 1 -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) 2>/dev/null | while read -r img; do
    img_name=$(basename "$img")
    img_name_no_ext="${img_name%.*}"
    label_file="$LABELS_TRAIN/${img_name_no_ext}.txt"
    if [ ! -f "$label_file" ]; then
        echo "  ⚠️  训练集缺少标注: $img_name"
        MISSING_TRAIN=$((MISSING_TRAIN + 1))
    fi
done

# 验证集
MISSING_VAL=0
find "$IMAGES_VAL" -maxdepth 1 -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) 2>/dev/null | while read -r img; do
    img_name=$(basename "$img")
    img_name_no_ext="${img_name%.*}"
    label_file="$LABELS_VAL/${img_name_no_ext}.txt"
    if [ ! -f "$label_file" ]; then
        echo "  ⚠️  验证集缺少标注: $img_name"
        MISSING_VAL=$((MISSING_VAL + 1))
    fi
done

if [ "$MISSING_TRAIN" -eq 0 ] && [ "$MISSING_VAL" -eq 0 ]; then
    echo "  ✅ 所有图片都有对应的标注文件"
fi

echo ""
echo "📋 类别文件检查："
if [ -f "$DATASET_DIR/classes.txt" ]; then
    echo "  ✅ classes.txt 存在"
    echo "  类别列表："
    cat "$DATASET_DIR/classes.txt" | sed 's/^/    - /'
else
    echo "  ⚠️  classes.txt 不存在"
fi

echo ""
echo "✅ 检查完成！"

