#!/usr/bin/env python3
"""
验证 YOLO 标注文件的质量和完整性
"""

import os
from pathlib import Path
import json

# 类别列表（应该与 classes.txt 一致）
CLASSES = ['red_rectangle', 'red_triangle', 'red_cube', 'blue_cube']

def validate_yolo_annotation(txt_file, image_path=None):
    """
    验证单个 YOLO 标注文件
    
    Returns:
        (is_valid, errors, warnings, info)
    """
    errors = []
    warnings = []
    info = {}
    
    if not os.path.exists(txt_file):
        errors.append(f"标注文件不存在: {txt_file}")
        return False, errors, warnings, info
    
    # 读取标注内容
    with open(txt_file, 'r') as f:
        lines = f.readlines()
    
    info['annotation_count'] = len([l for l in lines if l.strip()])
    
    if info['annotation_count'] == 0:
        warnings.append(f"标注文件为空（没有标注任何物体）")
    
    valid_annotations = 0
    invalid_lines = []
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        
        parts = line.split()
        if len(parts) != 5:
            invalid_lines.append(f"第 {line_num} 行格式错误: 应该有5个值，实际有 {len(parts)} 个")
            continue
        
        try:
            class_id = int(parts[0])
            center_x = float(parts[1])
            center_y = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])
            
            # 检查类别ID
            if class_id < 0 or class_id >= len(CLASSES):
                errors.append(f"第 {line_num} 行: 无效的类别ID {class_id}（应该在 0-{len(CLASSES)-1} 范围内）")
                continue
            
            # 检查坐标值（应该在 0-1 范围内）
            if not (0 <= center_x <= 1):
                errors.append(f"第 {line_num} 行: center_x {center_x} 超出范围 [0, 1]")
            if not (0 <= center_y <= 1):
                errors.append(f"第 {line_num} 行: center_y {center_y} 超出范围 [0, 1]")
            if not (0 <= width <= 1):
                errors.append(f"第 {line_num} 行: width {width} 超出范围 [0, 1]")
            if not (0 <= height <= 1):
                errors.append(f"第 {line_num} 行: height {height} 超出范围 [0, 1]")
            
            # 检查边界框是否在图片内
            x_min = center_x - width / 2
            x_max = center_x + width / 2
            y_min = center_y - height / 2
            y_max = center_y + height / 2
            
            if x_min < 0 or x_max > 1 or y_min < 0 or y_max > 1:
                warnings.append(f"第 {line_num} 行: 边界框超出图片范围")
            
            # 检查边界框大小（不能太小）
            if width < 0.01 or height < 0.01:
                warnings.append(f"第 {line_num} 行: 边界框太小（width={width:.4f}, height={height:.4f}）")
            
            valid_annotations += 1
            info[f'class_{class_id}'] = info.get(f'class_{class_id}', 0) + 1
            
        except ValueError as e:
            errors.append(f"第 {line_num} 行: 数值格式错误 - {e}")
            continue
    
    info['valid_annotations'] = valid_annotations
    if invalid_lines:
        errors.extend(invalid_lines)
    
    is_valid = len(errors) == 0
    return is_valid, errors, warnings, info

def check_dataset(dataset_dir, split='train'):
    """检查整个数据集"""
    images_dir = Path(dataset_dir) / 'images' / split
    labels_dir = Path(dataset_dir) / 'lables' / split
    
    if not images_dir.exists():
        print(f"❌ 错误: 图片目录不存在: {images_dir}")
        return False
    
    if not labels_dir.exists():
        print(f"❌ 错误: 标注目录不存在: {labels_dir}")
        return False
    
    # 获取所有图片文件
    image_files = []
    for ext in ['.png', '.jpg', '.jpeg']:
        image_files.extend(images_dir.glob(f'*{ext}'))
    
    # 获取所有标注文件
    label_files = list(labels_dir.glob('*.txt'))
    
    print(f"\n📊 数据集统计 ({split}):")
    print(f"   图片数量: {len(image_files)}")
    print(f"   标注文件数量: {len(label_files)}")
    
    if len(image_files) != len(label_files):
        print(f"   ⚠️  警告: 图片数量和标注文件数量不匹配！")
    
    # 验证每个标注文件
    total_errors = 0
    total_warnings = 0
    total_annotations = 0
    class_counts = {i: 0 for i in range(len(CLASSES))}
    
    print(f"\n🔍 验证标注文件...")
    
    for img_file in image_files:
        label_file = labels_dir / f"{img_file.stem}.txt"
        
        if not label_file.exists():
            print(f"   ⚠️  缺少标注文件: {label_file.name}")
            continue
        
        is_valid, errors, warnings, info = validate_yolo_annotation(label_file, img_file)
        
        if not is_valid:
            total_errors += len(errors)
            print(f"   ❌ {label_file.name}:")
            for err in errors[:3]:  # 只显示前3个错误
                print(f"      - {err}")
            if len(errors) > 3:
                print(f"      ... 还有 {len(errors) - 3} 个错误")
        
        if warnings:
            total_warnings += len(warnings)
            # 不显示警告，只统计
        
        total_annotations += info.get('valid_annotations', 0)
        for i in range(len(CLASSES)):
            class_counts[i] += info.get(f'class_{i}', 0)
    
    # 汇总统计
    print(f"\n✅ 验证结果:")
    print(f"   总标注框数: {total_annotations}")
    print(f"   错误数量: {total_errors}")
    print(f"   警告数量: {total_warnings}")
    
    if total_errors == 0:
        print(f"   ✅ 所有标注文件格式正确！")
    else:
        print(f"   ⚠️  发现 {total_errors} 个错误，请检查并修复")
    
    print(f"\n📋 类别统计:")
    for i, class_name in enumerate(CLASSES):
        count = class_counts[i]
        print(f"   {i}: {class_name} - {count} 个标注框")
    
    return total_errors == 0

def visualize_annotations(dataset_dir, split='train', num_samples=3):
    """可视化几个标注文件的内容"""
    labels_dir = Path(dataset_dir) / 'lables' / split
    images_dir = Path(dataset_dir) / 'images' / split
    
    label_files = list(labels_dir.glob('*.txt'))[:num_samples]
    
    print(f"\n📸 标注文件示例 ({split}):")
    for label_file in label_files:
        print(f"\n   {label_file.name}:")
        with open(label_file, 'r') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines[:5], 1):  # 只显示前5个标注
            parts = line.strip().split()
            if len(parts) == 5:
                class_id = int(parts[0])
                center_x, center_y = float(parts[1]), float(parts[2])
                width, height = float(parts[3]), float(parts[4])
                
                if class_id < len(CLASSES):
                    class_name = CLASSES[class_id]
                    print(f"      标注 {i}: {class_name} | 中心=({center_x:.3f}, {center_y:.3f}) | 尺寸=({width:.3f}, {height:.3f})")
                else:
                    print(f"      标注 {i}: [无效类别ID: {class_id}]")
        
        if len(lines) > 5:
            print(f"      ... 还有 {len(lines) - 5} 个标注")

if __name__ == '__main__':
    import sys
    
    dataset_dir = Path(__file__).parent
    if len(sys.argv) > 1:
        dataset_dir = Path(sys.argv[1])
    
    print("=" * 60)
    print("🔍 YOLO 标注文件验证工具")
    print("=" * 60)
    
    # 检查 classes.txt
    classes_file = dataset_dir / 'classes.txt'
    if classes_file.exists():
        with open(classes_file, 'r') as f:
            file_classes = [line.strip() for line in f if line.strip()]
        if file_classes != CLASSES:
            print(f"\n⚠️  警告: classes.txt 中的类别与脚本中的不一致")
            print(f"   脚本中: {CLASSES}")
            print(f"   文件中: {file_classes}")
    
    # 验证训练集
    train_ok = check_dataset(dataset_dir, 'train')
    
    # 验证验证集
    val_ok = check_dataset(dataset_dir, 'val')
    
    # 显示示例
    visualize_annotations(dataset_dir, 'train', num_samples=2)
    visualize_annotations(dataset_dir, 'val', num_samples=2)
    
    print("\n" + "=" * 60)
    if train_ok and val_ok:
        print("✅ 数据集验证通过！可以开始训练模型了。")
    else:
        print("⚠️  数据集存在一些问题，请检查上述错误信息。")
    print("=" * 60)








