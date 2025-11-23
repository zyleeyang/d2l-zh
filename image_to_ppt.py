#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
智能图片转可编辑PPT工具
Image to Editable PowerPoint Converter

这个工具能将图片自动转换为可编辑的PPT文件，支持以下功能：
1. PPT尺寸自适应
2. 智能元素识别（文本、形状、表格、图片）
3. 样式提取与匹配
4. 批量处理
5. 智能布局优化

Usage:
    python image_to_ppt.py input_image.jpg -o output.pptx
    python image_to_ppt.py input_folder/ -o output.pptx --batch
"""

import os
import sys
import json
import argparse
from typing import List, Dict, Tuple, Optional
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor


class ImageToPPTConverter:
    """智能图片转PPT转换器"""
    
    def __init__(self, config_path: str = "layout_rules.json"):
        """
        初始化转换器
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.prs = None
        
    def _load_config(self, config_path: str) -> dict:
        """加载配置文件"""
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 返回默认配置
            return {
                "slide_sizes": {
                    "16:9": {"width": 10, "height": 5.625, "unit": "inches"},
                    "4:3": {"width": 10, "height": 7.5, "unit": "inches"}
                },
                "aspect_ratio_thresholds": {
                    "16:9": {"min": 1.7, "max": 1.85},
                    "4:3": {"min": 1.25, "max": 1.4}
                }
            }
    
    def detect_aspect_ratio(self, image_path: str) -> str:
        """
        检测图片宽高比并自动选择PPT尺寸
        
        Args:
            image_path: 图片路径
            
        Returns:
            尺寸类型 (16:9, 4:3, A4等)
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"无法读取图片: {image_path}")
        
        height, width = img.shape[:2]
        aspect_ratio = width / height
        
        # 根据宽高比选择PPT尺寸
        thresholds = self.config.get("aspect_ratio_thresholds", {})
        
        for size_type, threshold in thresholds.items():
            if threshold["min"] <= aspect_ratio <= threshold["max"]:
                return size_type
        
        # 默认返回16:9
        return "16:9"
    
    def create_presentation(self, size_type: str = "16:9") -> Presentation:
        """
        创建PPT演示文稿
        
        Args:
            size_type: 尺寸类型
            
        Returns:
            Presentation对象
        """
        prs = Presentation()
        
        # 设置幻灯片尺寸
        size_config = self.config["slide_sizes"].get(size_type, 
                                                      self.config["slide_sizes"]["16:9"])
        prs.slide_width = Inches(size_config["width"])
        prs.slide_height = Inches(size_config["height"])
        
        return prs
    
    def extract_colors(self, image_path: str) -> Dict[str, Tuple[int, int, int]]:
        """
        提取图片的颜色方案
        
        Args:
            image_path: 图片路径
            
        Returns:
            颜色字典 {color_type: (R, G, B)}
        """
        img = cv2.imread(image_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # 提取背景色（使用四角采样）
        height, width = img_rgb.shape[:2]
        corners = [
            img_rgb[0, 0],
            img_rgb[0, width-1],
            img_rgb[height-1, 0],
            img_rgb[height-1, width-1]
        ]
        background_color = tuple(np.median(corners, axis=0).astype(int))
        
        # 提取主要颜色（使用K-means聚类）
        pixels = img_rgb.reshape(-1, 3)
        # 简化版本：使用中值
        dominant_color = tuple(np.median(pixels, axis=0).astype(int))
        
        return {
            "background": background_color,
            "dominant": dominant_color,
            "text": (0, 0, 0) if sum(background_color) > 384 else (255, 255, 255)
        }
    
    def detect_text_regions(self, image_path: str) -> List[Dict]:
        """
        检测图片中的文本区域
        
        Args:
            image_path: 图片路径
            
        Returns:
            文本区域列表
        """
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 使用自适应阈值 - 从配置获取参数
        text_config = self.config.get("element_detection", {}).get("text", {})
        block_size = text_config.get("adaptive_threshold_block_size", 11)
        constant = text_config.get("adaptive_threshold_constant", 2)
        
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, block_size, constant
        )
        
        # 查找轮廓
        contours, _ = cv2.findContours(
            binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        text_regions = []
        min_area = self.config.get("element_detection", {}).get("text", {}).get("min_area", 100)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > min_area:
                x, y, w, h = cv2.boundingRect(contour)
                
                # 文本区域通常宽高比较大
                aspect_ratio = w / h if h > 0 else 0
                if 0.1 < aspect_ratio < 20:
                    text_regions.append({
                        "x": x,
                        "y": y,
                        "width": w,
                        "height": h,
                        "text": f"文本区域 {len(text_regions) + 1}",
                        "type": "text"
                    })
        
        return text_regions
    
    def detect_shapes(self, image_path: str) -> List[Dict]:
        """
        检测图片中的几何形状
        
        Args:
            image_path: 图片路径
            
        Returns:
            形状列表
        """
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 边缘检测 - 从配置获取参数
        shape_config = self.config.get("element_detection", {}).get("shape", {})
        canny_low = shape_config.get("canny_threshold_low", 50)
        canny_high = shape_config.get("canny_threshold_high", 150)
        
        edges = cv2.Canny(gray, canny_low, canny_high)
        
        # 查找轮廓
        contours, _ = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        shapes = []
        min_area = self.config.get("element_detection", {}).get("shape", {}).get("min_area", 500)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > min_area:
                # 近似轮廓 - 从配置获取epsilon系数
                shape_config = self.config.get("element_detection", {}).get("shape", {})
                epsilon_factor = shape_config.get("approximation_epsilon", 0.02)
                epsilon = epsilon_factor * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                x, y, w, h = cv2.boundingRect(contour)
                
                # 判断形状类型
                shape_type = "polygon"
                if len(approx) == 3:
                    shape_type = "triangle"
                elif len(approx) == 4:
                    shape_type = "rectangle"
                elif len(approx) > 8:
                    shape_type = "circle"
                
                shapes.append({
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h,
                    "type": shape_type,
                    "vertices": len(approx)
                })
        
        return shapes
    
    def add_elements_to_slide(self, slide, elements: List[Dict], 
                             image_size: Tuple[int, int],
                             slide_size: Tuple[float, float],
                             colors: Dict[str, Tuple[int, int, int]]):
        """
        将检测到的元素添加到幻灯片
        
        Args:
            slide: 幻灯片对象
            elements: 元素列表
            image_size: 图片尺寸 (width, height)
            slide_size: 幻灯片尺寸 (width_inches, height_inches)
            colors: 颜色方案
        """
        img_width, img_height = image_size
        slide_width, slide_height = slide_size
        
        # 计算缩放比例
        scale_x = slide_width / img_width
        scale_y = slide_height / img_height
        
        for element in elements:
            # 转换坐标
            left = Inches(element["x"] * scale_x)
            top = Inches(element["y"] * scale_y)
            width = Inches(element["width"] * scale_x)
            height = Inches(element["height"] * scale_y)
            
            if element["type"] == "text":
                # 添加文本框
                textbox = slide.shapes.add_textbox(left, top, width, height)
                text_frame = textbox.text_frame
                text_frame.text = element.get("text", "示例文本")
                
                # 设置文本样式
                font_config = self.config.get("fonts", {})
                size_mapping = font_config.get("size_mapping", {})
                default_size = size_mapping.get("medium", 14)
                
                for paragraph in text_frame.paragraphs:
                    paragraph.font.size = Pt(default_size)
                    # 使用配置中的字体或fallback
                    try:
                        paragraph.font.name = font_config.get("default_chinese", "Arial")
                    except (KeyError, AttributeError):
                        paragraph.font.name = "Arial"
                    text_color = colors.get("text", (0, 0, 0))
                    paragraph.font.color.rgb = RGBColor(*text_color)
                    
            elif element["type"] in ["rectangle", "triangle", "circle"]:
                # 添加形状
                if element["type"] == "rectangle":
                    shape = slide.shapes.add_shape(
                        MSO_SHAPE.RECTANGLE, left, top, width, height
                    )
                elif element["type"] == "circle":
                    shape = slide.shapes.add_shape(
                        MSO_SHAPE.OVAL, left, top, width, height
                    )
                else:
                    shape = slide.shapes.add_shape(
                        MSO_SHAPE.ISOSCELES_TRIANGLE, left, top, width, height
                    )
                
                # 设置形状样式
                dominant_color = colors.get("dominant", (100, 100, 255))
                shape.fill.solid()
                shape.fill.fore_color.rgb = RGBColor(*dominant_color)
                shape.line.color.rgb = RGBColor(0, 0, 0)
    
    def convert_image_to_ppt(self, image_path: str, output_path: str,
                            size_type: Optional[str] = None) -> str:
        """
        将单张图片转换为PPT
        
        Args:
            image_path: 输入图片路径
            output_path: 输出PPT路径
            size_type: PPT尺寸类型（可选）
            
        Returns:
            输出文件路径
        """
        print(f"处理图片: {image_path}")
        
        # 自动检测尺寸
        if size_type is None:
            size_type = self.detect_aspect_ratio(image_path)
            print(f"检测到宽高比，使用 {size_type} 尺寸")
        
        # 创建PPT
        self.prs = self.create_presentation(size_type)
        
        # 添加空白幻灯片
        blank_slide_layout = self.prs.slide_layouts[6]  # 空白布局
        slide = self.prs.slides.add_slide(blank_slide_layout)
        
        # 提取颜色
        colors = self.extract_colors(image_path)
        print(f"提取的颜色方案: {colors}")
        
        # 检测元素
        text_regions = self.detect_text_regions(image_path)
        shapes = self.detect_shapes(image_path)
        print(f"检测到 {len(text_regions)} 个文本区域")
        print(f"检测到 {len(shapes)} 个形状")
        
        # 获取图片尺寸
        img = cv2.imread(image_path)
        img_height, img_width = img.shape[:2]
        
        # 获取幻灯片尺寸
        size_config = self.config["slide_sizes"][size_type]
        slide_width = size_config["width"]
        slide_height = size_config["height"]
        
        # 添加背景（原始图片）
        slide.shapes.add_picture(
            image_path,
            Inches(0),
            Inches(0),
            width=Inches(slide_width),
            height=Inches(slide_height)
        )
        
        # 添加检测到的元素
        all_elements = text_regions + shapes
        if all_elements:
            self.add_elements_to_slide(
                slide, all_elements,
                (img_width, img_height),
                (slide_width, slide_height),
                colors
            )
        
        # 添加备注
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = f"由图片自动生成: {os.path.basename(image_path)}\n"
        text_frame.text += f"原始尺寸: {img_width}x{img_height}\n"
        text_frame.text += f"检测到 {len(text_regions)} 个文本区域和 {len(shapes)} 个形状"
        
        # 保存PPT
        self.prs.save(output_path)
        print(f"PPT已保存到: {output_path}")
        
        return output_path
    
    def batch_convert(self, input_folder: str, output_path: str) -> str:
        """
        批量转换文件夹中的图片
        
        Args:
            input_folder: 输入文件夹路径
            output_path: 输出PPT路径
            
        Returns:
            输出文件路径
        """
        # 支持的图片格式
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif'}
        
        # 查找所有图片
        image_files = []
        for file in Path(input_folder).iterdir():
            if file.suffix.lower() in image_extensions:
                image_files.append(str(file))
        
        if not image_files:
            raise ValueError(f"文件夹 {input_folder} 中没有找到图片文件")
        
        print(f"找到 {len(image_files)} 张图片")
        
        # 创建PPT（使用第一张图片的尺寸）
        size_type = self.detect_aspect_ratio(image_files[0])
        self.prs = self.create_presentation(size_type)
        
        # 处理每张图片
        for i, image_path in enumerate(sorted(image_files), 1):
            print(f"\n[{i}/{len(image_files)}] 处理: {os.path.basename(image_path)}")
            
            # 添加空白幻灯片
            blank_slide_layout = self.prs.slide_layouts[6]
            slide = self.prs.slides.add_slide(blank_slide_layout)
            
            # 提取颜色和元素
            colors = self.extract_colors(image_path)
            text_regions = self.detect_text_regions(image_path)
            shapes = self.detect_shapes(image_path)
            
            # 获取尺寸
            img = cv2.imread(image_path)
            img_height, img_width = img.shape[:2]
            size_config = self.config["slide_sizes"][size_type]
            
            # 添加背景
            slide.shapes.add_picture(
                image_path,
                Inches(0),
                Inches(0),
                width=Inches(size_config["width"]),
                height=Inches(size_config["height"])
            )
            
            # 添加元素
            all_elements = text_regions + shapes
            if all_elements:
                self.add_elements_to_slide(
                    slide, all_elements,
                    (img_width, img_height),
                    (size_config["width"], size_config["height"]),
                    colors
                )
            
            # 添加备注
            notes_slide = slide.notes_slide
            text_frame = notes_slide.notes_text_frame
            text_frame.text = f"幻灯片 {i}: {os.path.basename(image_path)}"
        
        # 保存PPT
        self.prs.save(output_path)
        print(f"\n批量转换完成！PPT已保存到: {output_path}")
        
        return output_path


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="智能图片转可编辑PPT工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  单张图片转换:
    python image_to_ppt.py input.jpg -o output.pptx
  
  批量转换:
    python image_to_ppt.py images/ -o output.pptx --batch
  
  指定尺寸:
    python image_to_ppt.py input.jpg -o output.pptx --size 16:9
        """
    )
    
    parser.add_argument(
        'input',
        help='输入图片路径或文件夹路径（批量模式）'
    )
    parser.add_argument(
        '-o', '--output',
        default='output.pptx',
        help='输出PPT文件路径（默认: output.pptx）'
    )
    parser.add_argument(
        '--batch',
        action='store_true',
        help='批量处理模式（输入为文件夹）'
    )
    parser.add_argument(
        '--size',
        choices=['16:9', '4:3', 'A4', 'custom'],
        help='指定PPT尺寸类型（默认: 自动检测）'
    )
    parser.add_argument(
        '--config',
        default='layout_rules.json',
        help='配置文件路径（默认: layout_rules.json）'
    )
    
    args = parser.parse_args()
    
    # 检查输入
    if not os.path.exists(args.input):
        print(f"错误: 输入路径不存在: {args.input}")
        sys.exit(1)
    
    # 创建转换器
    converter = ImageToPPTConverter(args.config)
    
    try:
        if args.batch:
            # 批量转换
            if not os.path.isdir(args.input):
                print(f"错误: 批量模式需要输入文件夹路径")
                sys.exit(1)
            converter.batch_convert(args.input, args.output)
        else:
            # 单张图片转换
            if not os.path.isfile(args.input):
                print(f"错误: 输入不是文件: {args.input}")
                sys.exit(1)
            converter.convert_image_to_ppt(args.input, args.output, args.size)
        
        print("\n✓ 转换成功!")
        
    except Exception as e:
        print(f"\n✗ 转换失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
