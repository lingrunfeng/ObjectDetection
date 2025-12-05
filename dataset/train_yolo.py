#!/usr/bin/env python3
"""
训练自定义 YOLO 模型的脚本
"""

import os
from pathlib import Path
from ultralytics import YOLO

# 数据集配置
DATASET_DIR = Path(__file__).parent
DATA_YAML = DATASET_DIR / "data.yaml"

def main():
    print("=" * 60)
    print("🚀 开始训练 YOLO 模型")
    print("=" * 60)
    print()
    
    # 检查数据集配置
    if not DATA_YAML.exists():
        print(f"❌ 错误: 找不到数据集配置文件: {DATA_YAML}")
        return
    
    print(f"📁 数据集目录: {DATASET_DIR}")
    print(f"📄 配置文件: {DATA_YAML}")
    print()
    
    # 选择模型（yolov8n 是最小的，训练最快）
    # 可选: yolov8n, yolov8s, yolov8m, yolov8l, yolov8x
    model_size = "n"  # n=nanos, s=small, m=medium, l=large, x=xlarge
    
    print(f"🤖 使用模型: YOLOv8{model_size}")
    print()
    
    # 加载预训练模型
    model = YOLO(f'yolov8{model_size}.pt')
    
    print("=" * 60)
    print("📊 训练参数:")
    print("=" * 60)
    print(f"  数据集: {DATA_YAML}")
    print(f"  模型: yolov8{model_size}.pt")
    print(f"  Epochs: 100 (默认)")
    print(f"  图片大小: 640 (默认)")
    print(f"  批次大小: 16 (默认)")
    print()
    print("💡 提示: 训练过程中会显示进度，训练结果保存在 runs/detect/train/")
    print("=" * 60)
    print()
    
    # 开始训练
    results = model.train(
        data=str(DATA_YAML),      # 数据集配置文件
        epochs=100,                # 训练轮数
        imgsz=640,                 # 输入图片大小
        batch=16,                  # 批次大小（根据GPU内存调整）
        name='blocks_detection',   # 训练任务名称
        patience=50,               # 早停耐心值（50轮无改善则停止）
        save=True,                 # 保存检查点
        plots=True,                # 生成训练曲线图
    )
    
    print()
    print("=" * 60)
    print("✅ 训练完成！")
    print("=" * 60)
    print()
    print(f"📁 训练结果保存在: {results.save_dir}")
    print(f"📄 最佳模型: {results.save_dir}/weights/best.pt")
    print(f"📄 最后一轮模型: {results.save_dir}/weights/last.pt")
    print()
    print("💡 下一步:")
    print("   1. 查看训练结果: 打开 runs/detect/train/ 目录")
    print("   2. 使用最佳模型进行推理:")
    print(f"      model = YOLO('{results.save_dir}/weights/best.pt')")
    print("   3. 在 ROS2 中使用: 将 best.pt 复制到项目根目录")
    print()

if __name__ == '__main__':
    main()








