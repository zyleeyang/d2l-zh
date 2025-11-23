#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
编程接口示例：如何在Python代码中使用图片转PPT工具

这个文件展示了如何将image_to_ppt工具集成到您的Python项目中
"""

# 注意：运行此示例前需要安装所需依赖
# pip install -r requirements.txt

def example_1_basic_usage():
    """示例1: 基本用法 - 转换单张图片"""
    print("示例1: 基本用法")
    print("-" * 40)
    
    from image_to_ppt import ImageToPPTConverter
    
    # 创建转换器实例
    converter = ImageToPPTConverter()
    
    # 转换单张图片
    try:
        output_path = converter.convert_image_to_ppt(
            image_path="your_image.jpg",
            output_path="output.pptx"
        )
        print(f"成功生成PPT: {output_path}")
    except Exception as e:
        print(f"错误: {e}")
    
    print()


def example_2_custom_size():
    """示例2: 指定PPT尺寸"""
    print("示例2: 指定PPT尺寸")
    print("-" * 40)
    
    from image_to_ppt import ImageToPPTConverter
    
    converter = ImageToPPTConverter()
    
    # 使用16:9宽屏格式
    try:
        output_path = converter.convert_image_to_ppt(
            image_path="your_image.jpg",
            output_path="widescreen.pptx",
            size_type="16:9"
        )
        print(f"生成16:9格式PPT: {output_path}")
    except Exception as e:
        print(f"错误: {e}")
    
    print()


def example_3_batch_conversion():
    """示例3: 批量转换"""
    print("示例3: 批量转换文件夹")
    print("-" * 40)
    
    from image_to_ppt import ImageToPPTConverter
    
    converter = ImageToPPTConverter()
    
    # 批量转换整个文件夹
    try:
        output_path = converter.batch_convert(
            input_folder="./images/",
            output_path="batch_output.pptx"
        )
        print(f"批量转换完成: {output_path}")
    except Exception as e:
        print(f"错误: {e}")
    
    print()


def example_4_custom_config():
    """示例4: 使用自定义配置"""
    print("示例4: 使用自定义配置")
    print("-" * 40)
    
    from image_to_ppt import ImageToPPTConverter
    
    # 使用自定义配置文件
    converter = ImageToPPTConverter(config_path="my_custom_config.json")
    
    try:
        output_path = converter.convert_image_to_ppt(
            image_path="your_image.jpg",
            output_path="custom_output.pptx"
        )
        print(f"使用自定义配置生成: {output_path}")
    except Exception as e:
        print(f"错误: {e}")
    
    print()


def example_5_inspect_elements():
    """示例5: 检查检测到的元素"""
    print("示例5: 检查检测到的元素")
    print("-" * 40)
    
    from image_to_ppt import ImageToPPTConverter
    
    converter = ImageToPPTConverter()
    
    # 检测元素但不生成PPT
    try:
        image_path = "your_image.jpg"
        
        # 检测文本区域
        text_regions = converter.detect_text_regions(image_path)
        print(f"检测到 {len(text_regions)} 个文本区域")
        for i, region in enumerate(text_regions[:3], 1):
            print(f"  文本区域 {i}: {region}")
        
        # 检测形状
        shapes = converter.detect_shapes(image_path)
        print(f"\n检测到 {len(shapes)} 个形状")
        for i, shape in enumerate(shapes[:3], 1):
            print(f"  形状 {i}: 类型={shape['type']}, 位置=({shape['x']}, {shape['y']})")
        
        # 提取颜色
        colors = converter.extract_colors(image_path)
        print(f"\n颜色方案:")
        for color_type, rgb in colors.items():
            print(f"  {color_type}: RGB{rgb}")
        
    except Exception as e:
        print(f"错误: {e}")
    
    print()


def example_6_aspect_ratio_detection():
    """示例6: 检测图片宽高比"""
    print("示例6: 检测图片宽高比")
    print("-" * 40)
    
    from image_to_ppt import ImageToPPTConverter
    
    converter = ImageToPPTConverter()
    
    # 检测多张图片的宽高比
    image_files = [
        "image1.jpg",
        "image2.png",
        "image3.bmp"
    ]
    
    for image_path in image_files:
        try:
            size_type = converter.detect_aspect_ratio(image_path)
            print(f"{image_path}: 推荐使用 {size_type} 格式")
        except FileNotFoundError:
            print(f"{image_path}: 文件不存在")
        except Exception as e:
            print(f"{image_path}: 错误 - {e}")
    
    print()


def example_7_create_presentation_only():
    """示例7: 仅创建PPT框架（不添加图片）"""
    print("示例7: 创建PPT框架")
    print("-" * 40)
    
    from image_to_ppt import ImageToPPTConverter
    
    converter = ImageToPPTConverter()
    
    # 创建特定尺寸的空白演示文稿
    prs = converter.create_presentation(size_type="16:9")
    print(f"创建了 {prs.slide_width} x {prs.slide_height} 的演示文稿")
    
    # 可以手动添加幻灯片和内容
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    
    # 保存
    try:
        prs.save("empty_presentation.pptx")
        print("保存空白演示文稿: empty_presentation.pptx")
    except Exception as e:
        print(f"错误: {e}")
    
    print()


def example_8_error_handling():
    """示例8: 错误处理"""
    print("示例8: 正确的错误处理")
    print("-" * 40)
    
    from image_to_ppt import ImageToPPTConverter
    import os
    
    converter = ImageToPPTConverter()
    
    image_path = "input.jpg"
    output_path = "output.pptx"
    
    # 检查输入文件
    if not os.path.exists(image_path):
        print(f"错误: 输入图片不存在: {image_path}")
        return
    
    # 检查输出目录
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建输出目录: {output_dir}")
    
    # 执行转换
    try:
        result = converter.convert_image_to_ppt(image_path, output_path)
        print(f"转换成功: {result}")
    except ValueError as e:
        print(f"参数错误: {e}")
    except IOError as e:
        print(f"IO错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")
        import traceback
        traceback.print_exc()
    
    print()


def example_9_integration():
    """示例9: 集成到工作流"""
    print("示例9: 集成到工作流")
    print("-" * 40)
    
    from image_to_ppt import ImageToPPTConverter
    import os
    from pathlib import Path
    
    # 工作流：处理多个项目的图片
    projects = {
        "project_a": "./project_a/screenshots/",
        "project_b": "./project_b/designs/",
        "project_c": "./project_c/diagrams/"
    }
    
    converter = ImageToPPTConverter()
    
    for project_name, image_folder in projects.items():
        if not os.path.exists(image_folder):
            print(f"跳过 {project_name}: 文件夹不存在")
            continue
        
        output_file = f"{project_name}_presentation.pptx"
        
        try:
            converter.batch_convert(image_folder, output_file)
            print(f"✓ {project_name}: 生成 {output_file}")
        except Exception as e:
            print(f"✗ {project_name}: 失败 - {e}")
    
    print()


def main():
    """主函数 - 运行所有示例"""
    print("\n" + "=" * 60)
    print("图片转PPT工具 - 编程接口示例")
    print("=" * 60 + "\n")
    
    print("注意: 这些示例需要实际的图片文件才能运行")
    print("请确保提供正确的图片路径，或查看代码学习使用方法\n")
    
    # 示例列表
    examples = [
        ("基本用法", example_1_basic_usage),
        ("指定尺寸", example_2_custom_size),
        ("批量转换", example_3_batch_conversion),
        ("自定义配置", example_4_custom_config),
        ("检查元素", example_5_inspect_elements),
        ("宽高比检测", example_6_aspect_ratio_detection),
        ("创建框架", example_7_create_presentation_only),
        ("错误处理", example_8_error_handling),
        ("工作流集成", example_9_integration),
    ]
    
    # 显示菜单
    print("可用的示例:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\n提示: 修改示例代码中的图片路径以匹配您的文件")
    print("提示: 查看源代码了解详细的API用法")
    
    print("\n" + "=" * 60)
    print("查看完整文档: README_image_to_ppt.md")
    print("查看使用指南: USAGE_GUIDE_image_to_ppt.md")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
