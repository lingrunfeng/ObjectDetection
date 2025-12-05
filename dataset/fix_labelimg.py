#!/usr/bin/env python3
"""
修复 labelImg 启动问题的脚本
解决 Python 3.12 中 distutils 缺失的问题
"""

import sys
import os

# 修复 distutils 问题
try:
    import distutils
except ImportError:
    # Python 3.12+ 移除了 distutils，使用 setuptools 替代
    try:
        import setuptools
        # 为兼容性创建 distutils 别名
        sys.modules['distutils'] = setuptools
        sys.modules['distutils.spawn'] = setuptools
    except ImportError:
        print("错误: 需要安装 setuptools")
        print("运行: pip3 install --break-system-packages setuptools")
        sys.exit(1)

# 导入并启动 labelImg
try:
    from labelImg.labelImg import main
    if __name__ == '__main__':
        # 设置环境变量避免线程警告
        os.environ['QT_QPA_PLATFORM'] = 'xcb'
        main()
except Exception as e:
    print(f"启动 labelImg 时出错: {e}")
    print("\n尝试解决方案:")
    print("1. 安装 setuptools: pip3 install --break-system-packages setuptools")
    print("2. 或者使用 labelme: pip3 install --break-system-packages labelme")
    sys.exit(1)


