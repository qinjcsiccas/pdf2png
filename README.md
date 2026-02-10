# 📄 PDF 转换长图工具 | PDF to Long Image Conversion Tool

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.20+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

这是一个基于 **Streamlit** 和 **PyMuPDF** 开发的轻量级 PDF 处理工具。它能将 PDF 页面转换成高清晰度图片，并支持多页垂直拼接成“长图”，非常适合移动端阅读、学术交流或社交媒体分享。

A lightweight tool built with Streamlit and PyMuPDF. It converts PDF pages into high-definition images and supports merging multiple pages into a single vertical "long image."

---

## ✨ 功能亮点 | Key Features

* **🌍 国际化界面 (Bilingual UI)**: 全界面中英双语对照，美观专业。
* **🖼️ 自由拼接 (Vertical Merging)**: 自定义合并页数（例如：每 3 页拼成一张长图）。
* **🔍 极致清晰 (High Quality)**: 支持 1.0x - 5.0x 缩放因子，确保公式和图表清晰。
* **🎁 批量打包 (ZIP Packaging)**: 转换完成后，自动生成 ZIP 压缩包一键下载。

---

## 🚀 快速开始 | Quick Start

### 方式 A：直接访问 | Option A: Live Demo
[**👉 点击在线运行 / Click to Run Online**](https://share.streamlit.io/)

---

### 方式 B：本地运行 | Option B: Local Run

1. **克隆仓库 | Clone the Repo**
    ```bash
    git clone [https://github.com/YourUsername/pdf-to-long-image.git](https://github.com/YourUsername/pdf-to-long-image.git)
    cd pdf-to-long-image
    ```

2. **安装依赖 | Install Dependencies**
    ```bash
    pip install pymupdf pillow streamlit
    ```

3. **启动应用 | Run the App**
    ```bash
    streamlit run pdf_tool.py
    ```

---

## 🛠️ 技术栈 | Tech Stack

* **Streamlit**: 用于构建交互式 Web 界面。
* **PyMuPDF (fitz)**: 高效的 PDF 解析与渲染引擎。
* **Pillow (PIL)**: 用于图片的拼接与格式化处理。

---

## 📝 使用指南 | Usage Guide

1. **上传 (Upload)**: 将 PDF 文件拖入上传区域。
2. **设置 (Settings)**: 调整缩放因子和合并页数。
3. **转换 (Convert)**: 点击 `🚀 开始转换并打包`。
4. **下载 (Download)**: 点击生成的蓝色按钮下载 ZIP 包。

---

## 👨‍💻 作者 | Author

**Jincheng Qin**
- 📧 Email: [qinjincheng@mail.sic.ac.cn](mailto:qinjincheng@mail.sic.ac.cn)

---

## 📄 开源协议 | License
MIT License
