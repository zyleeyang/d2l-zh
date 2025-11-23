# 图片转PPT工具 - 使用指南

## 目录
1. [快速开始](#快速开始)
2. [安装步骤](#安装步骤)
3. [基本用法](#基本用法)
4. [高级功能](#高级功能)
5. [配置选项](#配置选项)
6. [常见问题](#常见问题)
7. [最佳实践](#最佳实践)

---

## 快速开始

### 最简单的使用方式

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 转换单张图片
python image_to_ppt.py your_image.jpg

# 输出: output.pptx
```

就这么简单！工具会自动：
- 检测图片尺寸并选择合适的PPT格式
- 识别图片中的文本和形状
- 提取颜色方案
- 生成可编辑的PPT文件

---

## 安装步骤

### 步骤 1: 检查Python版本

```bash
python --version
# 需要 Python 3.7 或更高版本
```

### 步骤 2: 安装核心依赖

```bash
pip install -r requirements.txt
```

这会安装以下核心库：
- `python-pptx`: PPT文件生成
- `opencv-python`: 图像处理
- `numpy`: 数值计算
- `Pillow`: 图片处理

### 步骤 3: 安装OCR支持（可选）

如果需要文字识别功能：

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-chi-sim  # 中文支持
pip install pytesseract
```

**macOS:**
```bash
brew install tesseract
pip install pytesseract
```

**Windows:**
1. 下载并安装 [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki)
2. 添加到系统PATH
3. `pip install pytesseract`

### 步骤 4: 验证安装

```bash
python test_image_to_ppt.py
```

如果看到 "✓ 所有测试通过!"，说明安装成功。

---

## 基本用法

### 1. 单张图片转换

```bash
python image_to_ppt.py input.jpg -o output.pptx
```

**参数说明:**
- `input.jpg`: 输入图片路径
- `-o output.pptx`: 输出PPT文件路径

**示例:**
```bash
# 转换JPEG图片
python image_to_ppt.py photo.jpg -o presentation.pptx

# 转换PNG图片
python image_to_ppt.py diagram.png -o slides.pptx

# 转换多种格式
python image_to_ppt.py screenshot.bmp -o demo.pptx
```

### 2. 批量转换文件夹

```bash
python image_to_ppt.py images/ -o album.pptx --batch
```

**功能:**
- 自动扫描文件夹中的所有图片
- 每张图片生成一页幻灯片
- 保持尺寸一致性

**示例:**
```bash
# 转换整个文件夹
python image_to_ppt.py ./photos/ -o photo_album.pptx --batch

# 转换项目截图
python image_to_ppt.py ./screenshots/ -o project_demo.pptx --batch
```

### 3. 指定PPT尺寸

```bash
python image_to_ppt.py input.jpg -o output.pptx --size 16:9
```

**可用尺寸:**
- `16:9`: 宽屏格式（推荐用于演示）
- `4:3`: 标准格式（传统投影仪）
- `A4`: A4纸张大小（打印）
- `custom`: 自定义尺寸（需修改配置文件）

**示例:**
```bash
# 宽屏演示
python image_to_ppt.py slide.jpg -o widescreen.pptx --size 16:9

# 标准格式
python image_to_ppt.py classic.jpg -o standard.pptx --size 4:3

# A4打印
python image_to_ppt.py poster.jpg -o print.pptx --size A4
```

---

## 高级功能

### 1. 使用自定义配置

```bash
python image_to_ppt.py input.jpg -o output.pptx --config my_rules.json
```

**创建自定义配置:**
```json
{
  "slide_sizes": {
    "custom": {
      "width": 12,
      "height": 9,
      "unit": "inches"
    }
  },
  "element_detection": {
    "text": {
      "min_area": 200
    }
  }
}
```

### 2. 查看详细帮助

```bash
python image_to_ppt.py --help
```

### 3. 运行功能演示

```bash
python demo_image_to_ppt.py
```

这会展示所有功能的说明和示例。

---

## 配置选项

### layout_rules.json 配置文件结构

#### 1. 幻灯片尺寸配置

```json
{
  "slide_sizes": {
    "16:9": {
      "width": 10,
      "height": 5.625,
      "unit": "inches",
      "description": "标准宽屏"
    }
  }
}
```

**可调整项:**
- `width`: 幻灯片宽度（英寸）
- `height`: 幻灯片高度（英寸）
- `unit`: 单位（默认"inches"）

#### 2. 宽高比阈值

```json
{
  "aspect_ratio_thresholds": {
    "16:9": {
      "min": 1.7,
      "max": 1.85
    }
  }
}
```

**说明:**
- 图片宽高比在此范围内会自动选择对应格式
- 可根据需求调整阈值

#### 3. 元素检测参数

```json
{
  "element_detection": {
    "text": {
      "min_area": 100,
      "ocr_confidence_threshold": 0.5
    },
    "shape": {
      "min_area": 500
    }
  }
}
```

**调整建议:**
- 提高 `min_area` 可减少小元素的检测
- 降低阈值可检测更多元素

#### 4. 布局优化选项

```json
{
  "layout_optimization": {
    "grid_snap": true,
    "auto_align": true,
    "merge_similar_text": true
  }
}
```

**选项说明:**
- `grid_snap`: 元素对齐到网格
- `auto_align`: 自动对齐相邻元素
- `merge_similar_text`: 合并相似文本区域

---

## 常见问题

### Q1: 安装时出错怎么办？

**A:** 确保Python版本 >= 3.7，然后逐个安装依赖：
```bash
pip install python-pptx
pip install opencv-python
pip install numpy
pip install Pillow
```

### Q2: 生成的PPT无法打开？

**A:** 检查：
1. 输出路径是否有写权限
2. python-pptx版本是否正确
3. 尝试用不同的PPT查看器打开

### Q3: 元素检测不准确？

**A:** 调整配置文件参数：
1. 修改 `min_area` 值
2. 调整图片质量和对比度
3. 使用更清晰的源图片

### Q4: 如何提高文字识别准确率？

**A:** 
1. 安装Tesseract OCR
2. 使用高分辨率图片
3. 确保文字清晰且对比度高

### Q5: 批量转换时程序卡住？

**A:**
1. 检查图片大小（建议 < 10MB）
2. 减少同时处理的图片数量
3. 确保有足够的内存

### Q6: 支持哪些图片格式？

**A:** 支持常见格式：
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)
- GIF (.gif)

---

## 最佳实践

### 1. 图片准备

**推荐:**
- 分辨率: 1920x1080 或更高
- 格式: PNG（最佳质量）或 JPEG
- 对比度: 高对比度便于元素检测
- 大小: 2-10MB 之间

**避免:**
- 过度压缩的图片
- 低分辨率图片（< 800x600）
- 模糊或失焦的图片

### 2. 批量处理技巧

**文件组织:**
```
project/
├── input_images/
│   ├── slide_01.png
│   ├── slide_02.png
│   └── slide_03.png
└── output/
    └── presentation.pptx
```

**命令:**
```bash
python image_to_ppt.py input_images/ -o output/presentation.pptx --batch
```

### 3. 配置优化

**对于文字较多的图片:**
```json
{
  "element_detection": {
    "text": {
      "min_area": 50
    }
  }
}
```

**对于图表和图形:**
```json
{
  "element_detection": {
    "shape": {
      "min_area": 1000
    }
  }
}
```

### 4. 工作流程建议

1. **准备阶段:**
   - 整理并命名图片文件
   - 检查图片质量
   - 确定需要的PPT格式

2. **转换阶段:**
   - 先测试单张图片
   - 调整配置参数
   - 再进行批量转换

3. **后期处理:**
   - 在PowerPoint中打开生成的文件
   - 手动调整需要修改的元素
   - 添加动画和过渡效果

### 5. 性能优化

**处理大量图片时:**
```bash
# 分批处理
python image_to_ppt.py batch1/ -o part1.pptx --batch
python image_to_ppt.py batch2/ -o part2.pptx --batch

# 然后在PowerPoint中合并
```

---

## 使用场景示例

### 场景 1: 设计稿转PPT

```bash
# 设计师提供的UI设计稿
python image_to_ppt.py ui_designs/ -o ui_presentation.pptx --batch --size 16:9
```

### 场景 2: 照片相册

```bash
# 旅游照片制作相册
python image_to_ppt.py vacation_photos/ -o trip_album.pptx --batch
```

### 场景 3: 会议记录

```bash
# 白板照片转成可编辑的PPT
python image_to_ppt.py whiteboard.jpg -o meeting_notes.pptx --size 4:3
```

### 场景 4: 教学资料

```bash
# 教材扫描图转PPT
python image_to_ppt.py textbook_pages/ -o lecture_slides.pptx --batch --size 4:3
```

---

## 进一步学习

### 查看源代码
- `image_to_ppt.py`: 主程序逻辑
- `layout_rules.json`: 配置示例
- `demo_image_to_ppt.py`: 功能演示

### 运行测试
```bash
python test_image_to_ppt.py
```

### 阅读文档
- `README_image_to_ppt.md`: 完整文档
- 本指南: 使用说明

---

## 获取帮助

如遇到问题：
1. 查看本文档的"常见问题"部分
2. 运行 `python image_to_ppt.py --help`
3. 查看 `demo_image_to_ppt.py` 的示例代码
4. 在GitHub上提交Issue

---

**祝使用愉快！** 🎉
