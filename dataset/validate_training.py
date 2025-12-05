#!/usr/bin/env python3
"""
验证训练结果和模型性能
"""

import os
from pathlib import Path
from ultralytics import YOLO
import json

def find_best_model():
    """查找训练好的最佳模型"""
    runs_dir = Path(__file__).parent / "runs" / "detect"
    
    if not runs_dir.exists():
        return None
    
    # 查找最新的训练结果
    train_dirs = sorted(runs_dir.glob("train*"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    if not train_dirs:
        return None
    
    latest_train = train_dirs[0]
    best_model = latest_train / "weights" / "best.pt"
    
    if best_model.exists():
        return best_model
    
    return None

def validate_model(model_path, test_image_dir):
    """在测试集上验证模型"""
    print(f"🔍 加载模型: {model_path}")
    model = YOLO(str(model_path))
    
    print(f"📸 在测试集上验证: {test_image_dir}")
    
    # 在验证集上验证
    results = model.val(
        data=str(Path(__file__).parent / "data.yaml"),
        split='val',
        imgsz=640,
        plots=True
    )
    
    print("\n" + "=" * 60)
    print("📊 验证结果:")
    print("=" * 60)
    print(f"  mAP50: {results.box.map50:.4f}")
    print(f"  mAP50-95: {results.box.map:.4f}")
    print()
    
    # 显示每个类别的性能
    if hasattr(results, 'names'):
        print("📋 各类别性能:")
        for i, name in results.names.items():
            if i < len(results.box.maps):
                map50 = results.box.maps50[i] if hasattr(results.box, 'maps50') else 0
                map = results.box.maps[i] if hasattr(results.box, 'maps') else 0
                print(f"  {name}: mAP50={map50:.4f}, mAP50-95={map:.4f}")
    
    return results

def test_inference(model_path, test_image):
    """在单张图片上测试推理"""
    print(f"\n🧪 测试推理: {test_image}")
    model = YOLO(str(model_path))
    
    results = model.predict(
        source=str(test_image),
        save=True,
        conf=0.25
    )
    
    print(f"\n✅ 检测结果已保存")
    return results

def main():
    print("=" * 60)
    print("🔍 模型验证工具")
    print("=" * 60)
    print()
    
    dataset_dir = Path(__file__).parent
    
    # 查找最佳模型
    best_model = find_best_model()
    
    if not best_model:
        print("❌ 未找到训练好的模型")
        print("   请先运行训练脚本: python3 train_yolo.py")
        return
    
    print(f"✅ 找到模型: {best_model}")
    print()
    
    # 验证模型
    val_dir = dataset_dir / "images" / "val"
    if val_dir.exists():
        results = validate_model(best_model, val_dir)
    else:
        print("⚠️  验证集目录不存在")
    
    # 在单张图片上测试
    test_images = list((dataset_dir / "images" / "val").glob("*.png"))[:1]
    if test_images:
        test_inference(best_model, test_images[0])
    
    print()
    print("=" * 60)
    print("✅ 验证完成！")
    print("=" * 60)
    print()
    print("💡 下一步:")
    print(f"   1. 查看验证结果图表: {best_model.parent.parent}")
    print(f"   2. 使用模型: model = YOLO('{best_model}')")
    print(f"   3. 在 ROS2 中使用: 复制 {best_model} 到项目根目录")
    print()

if __name__ == '__main__':
    main()








