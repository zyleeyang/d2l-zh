#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例脚本：演示图片转PPT工具的使用

这个脚本展示了如何使用image_to_ppt工具的各种功能
"""

import os
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from image_to_ppt import ImageToPPTConverter


def demo_basic_conversion():
    """示例1: 基础图片转换"""
    print("=" * 60)
    print("示例1: 基础图片转换")
    print("=" * 60)
    
    # 创建转换器
    converter = ImageToPPTConverter()
    
    # 假设有一个示例图片
    # 如果图片不存在，这只是演示代码结构
    example_image = "example_image.jpg"
    
    if os.path.exists(example_image):
        output_path = converter.convert_image_to_ppt(
            image_path=example_image,
            output_path="demo_output.pptx"
        )
        print(f"✓ 转换完成: {output_path}")
    else:
        print(f"ℹ 示例图片不存在: {example_image}")
        print("  请提供您自己的图片路径进行测试")


def demo_aspect_ratio_detection():
    """示例2: 演示宽高比自动检测"""
    print("\n" + "=" * 60)
    print("示例2: 宽高比自动检测")
    print("=" * 60)
    
    converter = ImageToPPTConverter()
    
    # 展示不同宽高比如何映射到PPT尺寸
    test_cases = [
        (1920, 1080, "预期: 16:9"),
        (1600, 1200, "预期: 4:3"),
        (2100, 2970, "预期: A4"),
    ]
    
    print("\n宽高比检测示例:")
    for width, height, expected in test_cases:
        aspect_ratio = width / height
        print(f"  图片尺寸 {width}x{height} (比例 {aspect_ratio:.2f}) -> {expected}")


def demo_color_extraction():
    """示例3: 演示颜色提取"""
    print("\n" + "=" * 60)
    print("示例3: 颜色方案提取")
    print("=" * 60)
    
    print("\n颜色提取功能说明:")
    print("  - 背景色: 通过四角采样估算")
    print("  - 主要颜色: 通过像素聚类分析")
    print("  - 文本颜色: 根据背景自动选择（确保可读性）")
    
    print("\n示例输出:")
    print("  {")
    print("    'background': (255, 255, 255),  # 白色背景")
    print("    'dominant': (51, 102, 204),     # 蓝色主色调")
    print("    'text': (0, 0, 0)               # 黑色文字")
    print("  }")


def demo_batch_conversion():
    """示例4: 演示批量转换"""
    print("\n" + "=" * 60)
    print("示例4: 批量转换演示")
    print("=" * 60)
    
    print("\n批量转换使用方法:")
    print("  converter = ImageToPPTConverter()")
    print("  converter.batch_convert(")
    print("      input_folder='./images/',")
    print("      output_path='batch_output.pptx'")
    print("  )")
    
    print("\n功能特点:")
    print("  - 自动扫描文件夹中的所有图片")
    print("  - 每张图片生成一页幻灯片")
    print("  - 自动保持尺寸一致性")
    print("  - 添加备注标识每页来源")


def demo_element_detection():
    """示例5: 演示元素检测"""
    print("\n" + "=" * 60)
    print("示例5: 元素检测功能")
    print("=" * 60)
    
    print("\n支持的元素类型:")
    print("  1. 文本区域")
    print("     - 使用轮廓检测识别文本块")
    print("     - 根据宽高比过滤")
    print("     - 输出: 坐标、尺寸、内容（可选OCR）")
    
    print("\n  2. 几何形状")
    print("     - 矩形: 4个顶点的多边形")
    print("     - 圆形: 8+个顶点的近似圆形")
    print("     - 三角形: 3个顶点的多边形")
    print("     - 输出: 类型、坐标、尺寸")
    
    print("\n  3. 表格区域（未来增强）")
    print("     - 检测水平和垂直线")
    print("     - 识别单元格结构")
    
    print("\n  4. 图片/图标区域（未来增强）")
    print("     - 基于纹理和边缘密度检测")


def demo_configuration():
    """示例6: 演示配置选项"""
    print("\n" + "=" * 60)
    print("示例6: 配置文件说明")
    print("=" * 60)
    
    print("\nlayout_rules.json 配置结构:")
    print("""
{
  "slide_sizes": {
    "16:9": {"width": 10, "height": 5.625}
  },
  "element_detection": {
    "text": {"min_area": 100},
    "shape": {"min_area": 500}
  },
  "layout_optimization": {
    "grid_snap": true,
    "auto_align": true
  }
}
    """)
    
    print("主要配置项:")
    print("  - slide_sizes: PPT尺寸预设")
    print("  - element_detection: 元素检测参数")
    print("  - layout_optimization: 布局优化选项")


def demo_advanced_features():
    """示例7: 演示高级功能"""
    print("\n" + "=" * 60)
    print("示例7: 高级功能")
    print("=" * 60)
    
    print("\n1. 智能布局优化")
    print("   - 网格对齐: 元素自动对齐到网格")
    print("   - 间距统一: 调整元素间距保持一致")
    print("   - 层级管理: 避免元素遮挡")
    
    print("\n2. 坐标精确映射")
    print("   - 图片坐标 -> PPT坐标自动换算")
    print("   - 保持相对位置和比例")
    print("   - 支持不同尺寸的精确转换")
    
    print("\n3. 样式保持")
    print("   - 颜色方案提取并应用")
    print("   - 字体大小智能映射")
    print("   - 形状样式保留")


def print_usage_summary():
    """打印使用总结"""
    print("\n" + "=" * 60)
    print("快速开始指南")
    print("=" * 60)
    
    print("\n最简单的使用方式:")
    print("  python image_to_ppt.py your_image.jpg")
    
    print("\n常用命令:")
    print("  # 单张图片转换")
    print("  python image_to_ppt.py input.jpg -o output.pptx")
    
    print("\n  # 批量转换")
    print("  python image_to_ppt.py images/ -o result.pptx --batch")
    
    print("\n  # 指定尺寸")
    print("  python image_to_ppt.py input.jpg -o output.pptx --size 16:9")
    
    print("\n获取帮助:")
    print("  python image_to_ppt.py --help")


def main():
    """主函数 - 运行所有示例"""
    print("\n")
    print("*" * 60)
    print("*" + " " * 58 + "*")
    print("*" + "   智能图片转可编辑PPT工具 - 功能演示   ".center(58) + "*")
    print("*" + " " * 58 + "*")
    print("*" * 60)
    print("\n")
    
    # 运行各个示例
    demo_basic_conversion()
    demo_aspect_ratio_detection()
    demo_color_extraction()
    demo_batch_conversion()
    demo_element_detection()
    demo_configuration()
    demo_advanced_features()
    print_usage_summary()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)
    print("\n详细文档请参考: README_image_to_ppt.md")
    print("配置文件: layout_rules.json")
    print("主程序: image_to_ppt.py")
    print("\n")


if __name__ == "__main__":
    main()
