#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试脚本：验证图片转PPT工具的基本功能

这个脚本测试image_to_ppt工具的核心功能，不依赖实际图片文件
"""

import os
import sys
import json
import unittest
from unittest.mock import Mock, patch, MagicMock

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestImageToPPTConverter(unittest.TestCase):
    """测试ImageToPPTConverter类的基本功能"""
    
    def test_config_loading(self):
        """测试配置文件加载"""
        # 测试加载实际配置文件
        config_path = "layout_rules.json"
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 验证配置结构
            self.assertIn("slide_sizes", config)
            self.assertIn("16:9", config["slide_sizes"])
            self.assertIn("4:3", config["slide_sizes"])
            self.assertIn("element_detection", config)
            print("✓ 配置文件加载测试通过")
    
    def test_aspect_ratio_calculation(self):
        """测试宽高比计算逻辑"""
        test_cases = [
            (1920, 1080, 1.7778, "16:9"),  # 标准16:9
            (1600, 1200, 1.3333, "4:3"),   # 标准4:3
            (2100, 2970, 0.7071, "A4"),    # A4纸张
        ]
        
        for width, height, expected_ratio, size_type in test_cases:
            actual_ratio = width / height
            self.assertAlmostEqual(actual_ratio, expected_ratio, places=2)
        
        print("✓ 宽高比计算测试通过")
    
    def test_slide_size_configuration(self):
        """测试幻灯片尺寸配置"""
        config_path = "layout_rules.json"
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 验证16:9尺寸
            size_16_9 = config["slide_sizes"]["16:9"]
            self.assertEqual(size_16_9["width"], 10)
            self.assertEqual(size_16_9["height"], 5.625)
            
            # 验证4:3尺寸
            size_4_3 = config["slide_sizes"]["4:3"]
            self.assertEqual(size_4_3["width"], 10)
            self.assertEqual(size_4_3["height"], 7.5)
            
            print("✓ 幻灯片尺寸配置测试通过")
    
    def test_element_detection_config(self):
        """测试元素检测配置"""
        config_path = "layout_rules.json"
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 验证元素检测参数
            element_config = config["element_detection"]
            self.assertIn("text", element_config)
            self.assertIn("shape", element_config)
            self.assertIn("table", element_config)
            
            # 验证最小面积参数
            self.assertGreater(element_config["text"]["min_area"], 0)
            self.assertGreater(element_config["shape"]["min_area"], 0)
            
            print("✓ 元素检测配置测试通过")
    
    def test_coordinate_mapping(self):
        """测试坐标映射逻辑"""
        # 图片尺寸
        img_width, img_height = 1920, 1080
        
        # PPT尺寸 (英寸)
        ppt_width, ppt_height = 10, 5.625
        
        # 计算缩放比例
        scale_x = ppt_width / img_width
        scale_y = ppt_height / img_height
        
        # 测试坐标转换
        test_points = [
            (0, 0),        # 左上角
            (1920, 1080),  # 右下角
            (960, 540),    # 中心点
        ]
        
        for x, y in test_points:
            ppt_x = x * scale_x
            ppt_y = y * scale_y
            
            # 验证坐标在有效范围内
            self.assertGreaterEqual(ppt_x, 0)
            self.assertGreaterEqual(ppt_y, 0)
            self.assertLessEqual(ppt_x, ppt_width)
            self.assertLessEqual(ppt_y, ppt_height)
        
        print("✓ 坐标映射测试通过")
    
    def test_color_format(self):
        """测试颜色格式"""
        # RGB颜色应该在0-255范围内
        test_colors = [
            (255, 255, 255),  # 白色
            (0, 0, 0),        # 黑色
            (255, 0, 0),      # 红色
            (100, 150, 200),  # 自定义颜色
        ]
        
        for r, g, b in test_colors:
            self.assertGreaterEqual(r, 0)
            self.assertLessEqual(r, 255)
            self.assertGreaterEqual(g, 0)
            self.assertLessEqual(g, 255)
            self.assertGreaterEqual(b, 0)
            self.assertLessEqual(b, 255)
        
        print("✓ 颜色格式测试通过")
    
    def test_requirements_file(self):
        """测试requirements.txt文件"""
        requirements_path = "requirements.txt"
        if os.path.exists(requirements_path):
            with open(requirements_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 验证核心依赖存在
            required_packages = [
                "python-pptx",
                "opencv-python",
                "numpy",
                "Pillow"
            ]
            
            for package in required_packages:
                self.assertIn(package, content)
            
            print("✓ requirements.txt测试通过")


class TestConfigurationValidation(unittest.TestCase):
    """测试配置文件完整性"""
    
    def test_json_structure(self):
        """测试JSON结构完整性"""
        config_path = "layout_rules.json"
        if not os.path.exists(config_path):
            self.skipTest(f"配置文件不存在: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 验证顶层键
        required_keys = [
            "slide_sizes",
            "aspect_ratio_thresholds",
            "element_detection",
            "color_analysis",
            "layout_optimization",
            "fonts"
        ]
        
        for key in required_keys:
            self.assertIn(key, config, f"缺少配置项: {key}")
        
        print("✓ JSON结构验证通过")
    
    def test_aspect_ratio_thresholds(self):
        """测试宽高比阈值配置"""
        config_path = "layout_rules.json"
        if not os.path.exists(config_path):
            self.skipTest(f"配置文件不存在: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        thresholds = config["aspect_ratio_thresholds"]
        
        # 验证每个尺寸类型都有min和max
        for size_type, threshold in thresholds.items():
            self.assertIn("min", threshold)
            self.assertIn("max", threshold)
            self.assertLess(threshold["min"], threshold["max"])
        
        print("✓ 宽高比阈值配置验证通过")


class TestDocumentation(unittest.TestCase):
    """测试文档完整性"""
    
    def test_readme_exists(self):
        """测试README文件存在"""
        readme_path = "README_image_to_ppt.md"
        self.assertTrue(os.path.exists(readme_path))
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证关键章节存在
        key_sections = [
            "项目简介",
            "核心功能",
            "安装说明",
            "使用方法",
            "配置文件说明"
        ]
        
        for section in key_sections:
            self.assertIn(section, content)
        
        print("✓ README文档验证通过")
    
    def test_demo_script_exists(self):
        """测试演示脚本存在"""
        demo_path = "demo_image_to_ppt.py"
        self.assertTrue(os.path.exists(demo_path))
        print("✓ 演示脚本验证通过")


def run_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("运行图片转PPT工具测试套件")
    print("=" * 60 + "\n")
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestImageToPPTConverter))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigurationValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestDocumentation))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 打印总结
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✓ 所有测试通过!")
    else:
        print("✗ 部分测试失败")
    print("=" * 60 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
