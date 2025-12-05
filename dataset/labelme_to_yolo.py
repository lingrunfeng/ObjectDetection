#!/usr/bin/env python3
"""
将 labelme 生成的 JSON 标注文件转换为 YOLO 格式的 TXT 文件
"""

import json
import os
from pathlib import Path

# 类别映射（必须与 classes.txt 中的顺序一致）
CLASSES = {
    'green_cube': 0,
    'purple_cube': 1,
    'blue_cube': 2,
    'yellow_cylinder': 3,
    'red_cube': 4
}

def convert_labelme_to_yolo(json_file_path, image_width, image_height):
    """
    将单个 labelme JSON 文件转换为 YOLO 格式字符串
    
    Args:
        json_file_path: JSON 文件路径
        image_width: 图片宽度
        image_height: 图片高度
    
    Returns:
        YOLO 格式的字符串（每行一个标注）
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 如果 JSON 中包含图片尺寸信息，使用它
    if 'imageWidth' in data:
        image_width = data['imageWidth']
    if 'imageHeight' in data:
        image_height = data['imageHeight']
    
    yolo_lines = []
    for shape in data.get('shapes', []):
        shape_type = shape['shape_type']
        label = shape['label']
        
        # 检查类别
        if label not in CLASSES:
            print(f"警告: 未知类别 '{label}'，跳过")
            continue
        
        class_id = CLASSES[label]
        points = shape['points']
        
        if len(points) < 2:
            print(f"警告: 标注点不足，跳过")
            continue
        
        # 处理矩形标注
        if shape_type == 'rectangle':
            x1, y1 = points[0]
            x2, y2 = points[1]
            
            x_min = min(x1, x2)
            x_max = max(x1, x2)
            y_min = min(y1, y2)
            y_max = max(y1, y2)
        
        # 处理多边形标注 - 计算边界框
        elif shape_type == 'polygon':
            # 找到所有点的最小和最大坐标
            x_coords = [p[0] for p in points]
            y_coords = [p[1] for p in points]
            
            x_min = min(x_coords)
            x_max = max(x_coords)
            y_min = min(y_coords)
            y_max = max(y_coords)
        
        else:
            print(f"警告: 不支持的标注类型 '{shape_type}'，跳过")
            continue
        
        # 转换为 YOLO 格式 (center_x, center_y, width, height) - 归一化到 0-1
        center_x = ((x_min + x_max) / 2) / image_width
        center_y = ((y_min + y_max) / 2) / image_height
        width = (x_max - x_min) / image_width
        height = (y_max - y_min) / image_height
        
        # 确保值在 [0, 1] 范围内
        center_x = max(0, min(1, center_x))
        center_y = max(0, min(1, center_y))
        width = max(0, min(1, width))
        height = max(0, min(1, height))
        
        yolo_lines.append(f"{class_id} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}")
    
    return '\n'.join(yolo_lines)

def batch_convert(json_dir, output_dir, image_dir=None):
    """
    批量转换 labelme JSON 文件为 YOLO 格式
    
    Args:
        json_dir: JSON 文件目录
        output_dir: 输出 TXT 文件目录
        image_dir: 图片目录（用于获取图片尺寸，可选）
    """
    json_dir = Path(json_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    json_files = list(json_dir.glob('*.json'))
    
    if not json_files:
        print(f"错误: 在 {json_dir} 中未找到 JSON 文件")
        return
    
    print(f"找到 {len(json_files)} 个 JSON 文件，开始转换...")
    
    converted = 0
    failed = 0
    
    for json_file in json_files:
        try:
            # 尝试从 JSON 中获取图片尺寸
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            image_width = data.get('imageWidth', 1920)  # 默认值
            image_height = data.get('imageHeight', 1080)  # 默认值
            
            # 如果 JSON 中没有尺寸信息，尝试从同名图片文件获取
            if image_dir and (image_width == 1920 or image_height == 1080):
                image_path = Path(image_dir) / json_file.stem
                for ext in ['.png', '.jpg', '.jpeg']:
                    img_file = image_path.with_suffix(ext)
                    if img_file.exists():
                        try:
                            from PIL import Image
                            img = Image.open(img_file)
                            image_width, image_height = img.size
                            break
                        except:
                            pass
            
            # 转换
            yolo_content = convert_labelme_to_yolo(json_file, image_width, image_height)
            
            # 保存为 TXT 文件
            output_file = output_dir / f"{json_file.stem}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(yolo_content)
            
            converted += 1
            if converted % 10 == 0:
                print(f"已转换: {converted}/{len(json_files)}")
        
        except Exception as e:
            print(f"错误: 转换 {json_file.name} 失败: {e}")
            failed += 1
    
    print(f"\n转换完成!")
    print(f"成功: {converted} 个文件")
    if failed > 0:
        print(f"失败: {failed} 个文件")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("用法:")
        print("  python3 labelme_to_yolo.py <json_dir> <output_dir> [image_dir]")
        print("")
        print("示例:")
        print("  python3 labelme_to_yolo.py lables/train lables/train images/train")
        sys.exit(1)
    
    json_dir = sys.argv[1]
    output_dir = sys.argv[2]
    image_dir = sys.argv[3] if len(sys.argv) > 3 else None
    
    batch_convert(json_dir, output_dir, image_dir)

