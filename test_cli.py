#!/usr/bin/env python3
"""
Test script for image-process CLI
"""

import os
import sys
import tempfile
from PIL import Image
import subprocess

def create_test_images():
    """创建测试图片"""
    # 创建第一张图片 (红色)
    img1 = Image.new('RGB', (100, 100), color='red')
    
    # 创建第二张图片 (蓝色)
    img2 = Image.new('RGB', (100, 100), color='blue')
    
    # 保存图片
    img1.save('test_img1.jpg')
    img2.save('test_img2.jpg')
    
    return ['test_img1.jpg', 'test_img2.jpg']

def test_cli():
    """测试CLI工具"""
    # 创建测试图片
    test_files = create_test_images()
    
    # 测试命令
    cmd = [
        sys.executable, '-m', 'image_process',
        '--files', test_files[0],
        '--files', test_files[1],
        '--output', 'test_output.jpg'
    ]
    
    # 运行命令
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # 打印输出和错误
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    
    # 检查结果
    if result.returncode != 0:
        print(f"命令执行失败: {result.stderr}")
        return False
    
    # 检查输出文件是否存在
    if not os.path.exists('test_output.jpg'):
        print("输出文件未创建")
        return False
    
    # 检查输出文件是否为有效图片
    try:
        output_img = Image.open('test_output.jpg')
        print(f"输出图片尺寸: {output_img.size}")
        output_img.close()
    except Exception as e:
        print(f"输出文件不是有效图片: {e}")
        return False
    
    # 清理测试文件
    for f in test_files:
        if os.path.exists(f):
            os.remove(f)
    if os.path.exists('test_output.jpg'):
        os.remove('test_output.jpg')
    
    print("CLI测试通过!")
    return True

if __name__ == "__main__":
    test_cli()