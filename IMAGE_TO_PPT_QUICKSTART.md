# 图片转PPT工具 - 快速参考

## 🚀 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 转换单张图片
python image_to_ppt.py input.jpg -o output.pptx

# 批量转换
python image_to_ppt.py images/ -o batch.pptx --batch
```

## 📚 文档索引

| 文档 | 说明 |
|------|------|
| [README_image_to_ppt.md](README_image_to_ppt.md) | 完整功能文档 |
| [USAGE_GUIDE_image_to_ppt.md](USAGE_GUIDE_image_to_ppt.md) | 详细使用指南 |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | 项目总结 |

## 📝 示例代码

| 文件 | 用途 |
|------|------|
| [demo_image_to_ppt.py](demo_image_to_ppt.py) | 功能演示 |
| [examples_image_to_ppt.py](examples_image_to_ppt.py) | 编程接口示例 |
| [test_image_to_ppt.py](test_image_to_ppt.py) | 单元测试 |

## 🔧 核心文件

- **image_to_ppt.py** - 主程序
- **layout_rules.json** - 配置文件
- **requirements.txt** - 依赖列表

## ✨ 主要功能

- ✅ 自动PPT尺寸适配
- ✅ 智能元素识别（文本、形状）
- ✅ 颜色和样式提取
- ✅ 批量处理
- ✅ 完全可配置
- ✅ 跨平台支持

## 🧪 测试

```bash
python test_image_to_ppt.py
# 结果: ✓ 所有11个测试通过
```

## 💡 常用命令

```bash
# 查看帮助
python image_to_ppt.py --help

# 指定尺寸
python image_to_ppt.py input.jpg -o output.pptx --size 16:9

# 使用自定义配置
python image_to_ppt.py input.jpg -o output.pptx --config my_config.json

# 运行演示
python demo_image_to_ppt.py
python examples_image_to_ppt.py
```

## 📦 技术栈

- Python 3.7+
- python-pptx (PPT生成)
- OpenCV (图像处理)
- NumPy (数值计算)
- Pillow (图片处理)

## 📄 许可证

MIT-0

---

**详细文档请查看**: [README_image_to_ppt.md](README_image_to_ppt.md)
