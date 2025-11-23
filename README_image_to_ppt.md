# 智能图片转可编辑PPT工具

## 项目简介

这是一个能将图片自动转换为可编辑PPT文件的智能工具，使用计算机视觉和图像处理技术实现元素识别和样式提取。

## 核心功能

### 一、基础功能模块

#### 1. PPT尺寸自适应
- 根据输入图片的宽高比例自动选择PPT幻灯片尺寸（16:9、4:3、A4等）
- 支持用户自定义尺寸或选择预设模板
- 智能检测并匹配最佳幻灯片尺寸

#### 2. 智能元素识别
使用CV技术检测图片中的以下元素：
- **文本区域**：标题、正文、项目符号
- **几何形状**：矩形、圆形、三角形、箭头等
- **表格区域**：含边框检测
- **图片/图标区域**：自动识别图像区域
- 输出每个元素的坐标位置和尺寸

#### 3. 样式提取与匹配
- 提取颜色方案（主题色、背景色、字体颜色）
- 识别字体大小和粗略的字体系列
- 检测形状的填充颜色和边框样式

### 二、技术实现

#### 1. 图像处理
- 使用 **OpenCV** 进行轮廓检测和区域分割
- 应用 **OCR**（Tesseract/PaddleOCR）提取文本内容和位置
- 采用深度学习模型（可选YOLO）进行版面分析

#### 2. PPT生成引擎
- 使用 **python-pptx** 库动态创建PPT
- 实现精准坐标映射（图片坐标→PPT坐标换算）
- 自动对齐系统（网格对齐、元素间距统一）

#### 3. 智能布局优化
- 自动矫正倾斜文本
- 合并相邻的相似样式文本区域
- 智能调整元素层级关系（避免遮挡）

### 三、输出保障

#### 1. 可编辑性保障
- 所有文本必须为可编辑状态（非图片形式）
- 保留形状的矢量属性支持二次修改
- 生成备注说明原始布局来源

#### 2. 文件结构
```
.
├── image_to_ppt.py           # 主程序
├── layout_rules.json         # 配置文件（包含尺寸映射规则）
├── requirements.txt          # 依赖文件
└── README_image_to_ppt.md   # 本文档
```

## 安装说明

### 系统要求
- Python 3.7+
- pip

### 安装依赖

```bash
pip install -r requirements.txt
```

### 可选依赖

如需使用OCR功能，需要安装Tesseract：

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-chi-sim  # 中文支持
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
下载并安装 [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki)

## 使用方法

### 基础用法

#### 单张图片转换
```bash
python image_to_ppt.py input.jpg -o output.pptx
```

#### 批量转换
```bash
python image_to_ppt.py images/ -o output.pptx --batch
```

#### 指定PPT尺寸
```bash
python image_to_ppt.py input.jpg -o output.pptx --size 16:9
```

### 命令行参数

```
usage: image_to_ppt.py [-h] [-o OUTPUT] [--batch] [--size {16:9,4:3,A4,custom}] [--config CONFIG] input

智能图片转可编辑PPT工具

positional arguments:
  input                 输入图片路径或文件夹路径（批量模式）

optional arguments:
  -h, --help            显示帮助信息
  -o OUTPUT, --output OUTPUT
                        输出PPT文件路径（默认: output.pptx）
  --batch               批量处理模式（输入为文件夹）
  --size {16:9,4:3,A4,custom}
                        指定PPT尺寸类型（默认: 自动检测）
  --config CONFIG       配置文件路径（默认: layout_rules.json）
```

### 使用示例

#### 示例 1: 转换单张图片（自动检测尺寸）
```bash
python image_to_ppt.py my_image.jpg -o presentation.pptx
```

#### 示例 2: 批量转换文件夹中的所有图片
```bash
python image_to_ppt.py ./my_images/ -o batch_output.pptx --batch
```

#### 示例 3: 指定16:9宽屏格式
```bash
python image_to_ppt.py poster.png -o widescreen.pptx --size 16:9
```

#### 示例 4: 使用自定义配置文件
```bash
python image_to_ppt.py input.jpg -o output.pptx --config my_config.json
```

## 配置文件说明

`layout_rules.json` 包含以下配置项：

### 幻灯片尺寸配置
```json
{
  "slide_sizes": {
    "16:9": {
      "width": 10,
      "height": 5.625,
      "unit": "inches"
    }
  }
}
```

### 元素检测配置
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

### 布局优化配置
```json
{
  "layout_optimization": {
    "grid_snap": true,
    "auto_align": true,
    "merge_similar_text": true
  }
}
```

## 功能特性详解

### 1. 自动尺寸检测
程序会根据输入图片的宽高比自动选择最合适的PPT尺寸：
- **16:9**：宽高比在 1.7 - 1.85 之间
- **4:3**：宽高比在 1.25 - 1.4 之间
- **A4**：宽高比在 0.65 - 0.75 之间

### 2. 元素识别算法

#### 文本区域检测
- 使用自适应阈值二值化
- 轮廓检测识别文本块
- 根据宽高比过滤非文本区域

#### 形状检测
- Canny边缘检测
- 轮廓近似识别形状类型
- 支持：矩形、圆形、三角形等

#### 颜色提取
- 四角采样估算背景色
- 像素聚类提取主要颜色
- 自动计算文本颜色（确保可读性）

### 3. 坐标映射系统

程序实现了精确的坐标转换：
```
PPT坐标 = 图片坐标 × (PPT尺寸 / 图片尺寸)
```

### 4. 可编辑性保障

生成的PPT文件中：
- 文本以文本框形式存在，可直接编辑
- 形状为矢量图形，可调整大小和样式
- 原始图片作为背景层，方便参考
- 备注中包含原始图片信息

## 增强功能

### 批量处理模式
支持一次处理多张图片，每张图片生成一页幻灯片：
```bash
python image_to_ppt.py ./photos/ -o album.pptx --batch
```

### 智能布局优化
- 自动对齐相邻元素
- 统一元素间距
- 优化层级关系避免遮挡

### 样式保持
- 提取并应用原图配色方案
- 智能字体大小映射
- 保持视觉一致性

## 技术架构

### 核心类：ImageToPPTConverter

主要方法：
- `detect_aspect_ratio()`: 检测图片宽高比
- `create_presentation()`: 创建PPT文档
- `extract_colors()`: 提取颜色方案
- `detect_text_regions()`: 检测文本区域
- `detect_shapes()`: 检测几何形状
- `add_elements_to_slide()`: 添加元素到幻灯片
- `convert_image_to_ppt()`: 单张图片转换
- `batch_convert()`: 批量转换

### 依赖库

核心依赖：
- `python-pptx`: PPT文件生成
- `opencv-python`: 图像处理
- `numpy`: 数值计算
- `Pillow`: 图片处理

可选依赖：
- `pytesseract`: OCR文字识别
- `paddleocr`: 中文OCR
- `scikit-image`: 高级图像处理

## 限制和注意事项

1. **OCR识别**：当前版本的文本识别基于轮廓检测，准确率取决于图片质量。如需更好的文字识别，建议安装OCR库。

2. **复杂布局**：对于非常复杂的布局，可能需要手动调整生成的PPT。

3. **图片质量**：建议使用清晰、对比度高的图片以获得最佳识别效果。

4. **性能**：批量处理大量高分辨率图片时可能需要较长时间。

## 故障排除

### 问题：无法导入cv2
**解决方案**：
```bash
pip install opencv-python
```

### 问题：生成的PPT无法打开
**解决方案**：
- 确保输出路径有写权限
- 检查python-pptx版本是否正确

### 问题：元素检测不准确
**解决方案**：
- 调整 `layout_rules.json` 中的检测参数
- 提高输入图片的清晰度和对比度

## 未来改进方向

1. **深度学习集成**
   - 集成YOLO进行更准确的版面分析
   - 使用深度学习模型进行表格检测

2. **交互式校正**
   - 提供GUI界面进行手动调整
   - 实时预览转换结果

3. **模板库**
   - 内置常用商务模板
   - 支持自定义模板导入

4. **高级OCR**
   - 完整集成OCR引擎
   - 支持多语言文字识别

5. **云服务支持**
   - 提供Web服务API
   - 支持在线批量处理

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 许可证

本项目遵循MIT-0许可证。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交Issue到GitHub仓库
- 发送邮件到项目维护者

## 致谢

本项目使用了以下开源库：
- python-pptx
- OpenCV
- NumPy
- Pillow

感谢所有贡献者和开源社区的支持！

---

**注意**: 本工具旨在辅助PPT创建，生成的文件可能需要人工审核和调整以达到最佳效果。
