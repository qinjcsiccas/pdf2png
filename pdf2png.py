import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import zipfile

# 页面配置 / Page Configuration
st.set_page_config(page_title="PDF to Long Image Tool", page_icon="📄")

# --- README 展示功能 / Show README Feature ---
# 使用 st.expander 实现平时关上、需要时展开的功能
with st.expander("📖 查看使用指南与项目说明 (Show Guide & README)"):
    st.markdown("""
    # 📄 PDF 转换长图工具 | PDF to Long Image Conversion Tool
    
    这是一个基于 **Streamlit** 和 **PyMuPDF** 开发的轻量级 PDF 处理工具。
    A lightweight tool to convert PDF pages into high-definition images or vertical long images.

    ---

    ### ✨ 功能亮点 | Key Features
    * **🌍 国际化界面 (Bilingual UI)**: 全界面中英双语对照。
    * **🖼️ 自由拼接 (Vertical Merging)**: 自定义合并页数。
    * **🔍 极致清晰 (High Quality)**: 支持 1.0x - 5.0x 缩放因子。
    * **🎁 批量打包 (ZIP Packaging)**: 一键下载所有生成的图片。

    ### 🚀 本地运行 | Local Run
    1. **安装依赖**: `pip install pymupdf pillow streamlit`
    2. **启动应用**: `streamlit run pdf_tool.py`

    ---
    **Author:** Jincheng Qin  
    **Email:** qinjincheng@mail.sic.ac.cn
    """)

# 自定义小字样式的 Markdown 函数
def bilingual_title(zh, en):
    st.markdown(f"### {zh}")
    st.markdown(f"<p style='font-size: 0.85rem; color: #666; margin-top: -15px;'>{en}</p>", unsafe_allow_html=True)

def bilingual_text(zh, en):
    return f"{zh} \n ({en})"

# 主标题区域
st.title("📄 PDF 转换长图工具")
st.markdown("<p style='font-size: 1.1rem; color: #666; margin-top: -20px;'>PDF to Long Image Conversion Tool</p>", unsafe_allow_html=True)
st.write("---")

# --- 侧边栏配置 / Sidebar Settings ---
st.sidebar.header("转换设置")
st.sidebar.markdown("<p style='font-size: 0.8rem; color: #666; margin-top: -15px;'>Conversion Settings</p>", unsafe_allow_html=True)

zoom_level = st.sidebar.slider("图片清晰度 (缩放因子)", 1.0, 5.0, 3.0, 0.5)
st.sidebar.markdown("<p style='font-size: 0.8rem; color: #666; margin-top: -25px;'>Image Quality (Zoom Factor)</p>", unsafe_allow_html=True)

merge_num = st.sidebar.number_input("合并页数 (多少页拼成一张图)", min_value=1, value=1, step=1)
st.sidebar.markdown("<p style='font-size: 0.8rem; color: #666; margin-top: -10px;'>Pages per Image (Merge Count)</p>", unsafe_allow_html=True)

# --- 文件上传 / File Uploader ---
st.subheader("选择 PDF 文件")
st.markdown("<p style='font-size: 0.85rem; color: #666; margin-top: -15px;'>Choose a PDF file</p>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")

if uploaded_file is not None:
    raw_name = uploaded_file.name
    base_name = raw_name.rsplit('.', 1)[0] if '.' in raw_name else raw_name
    file_bytes = uploaded_file.read()
    
    # 顶部下载按钮占位符
    top_download_place = st.empty()
    
    btn_label = "🚀 开始转换并打包 \n (Start Conversion & Pack)"
    if st.button(btn_label, use_container_width=True):
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            total_pages = len(doc)
            
            all_images = [] 
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            zoom_matrix = fitz.Matrix(zoom_level, zoom_level)
            
            st.write("---")
            st.subheader("预览")
            st.markdown("<p style='font-size: 0.85rem; color: #666; margin-top: -15px;'>Preview</p>", unsafe_allow_html=True)

            for i in range(0, total_pages, merge_num):
                end_page = min(i + merge_num, total_pages)
                status_text.markdown(f"**正在处理 (Processing):** {i+1} - {end_page} / {total_pages}")
                
                pil_images = []
                max_width = 0
                total_height = 0

                for p_num in range(i, end_page):
                    page = doc[p_num]
                    pix = page.get_pixmap(matrix=zoom_matrix, alpha=False)
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    pil_images.append(img)
                    max_width = max(max_width, img.width)
                    total_height += img.height
                
                if len(pil_images) == 1:
                    final_img = pil_images[0]
                else:
                    final_img = Image.new('RGB', (max_width, total_height), (255, 255, 255))
                    current_y = 0
                    for img in pil_images:
                        final_img.paste(img, (0, current_y))
                        current_y += img.height

                buf = io.BytesIO()
                final_img.save(buf, format="PNG", quality=95)
                img_data = buf.getvalue()
                
                img_file_name = f"{base_name}_p{i+1}-{end_page}.png"
                all_images.append((img_file_name, img_data))
                
                st.image(img_data, caption=img_file_name)
                progress_bar.progress(end_page / total_pages)

            doc.close()
            status_text.success("✅ 转换完成！ (Conversion Finished!)")

            # --- 打包 ZIP ---
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for name, data in all_images:
                    zip_file.writestr(name, data)
            
            zip_data = zip_buffer.getvalue()
            zip_filename = f"{base_name}_images.zip"

            # 顶部和底部下载按钮
            download_btn_text = "🎁 点击下载所有图片压缩包 (Download All Images ZIP)"
            
            top_download_place.download_button(
                label=download_btn_text,
                data=zip_data,
                file_name=zip_filename,
                mime="application/zip",
                use_container_width=True,
                key="top_dl"
            )

            st.download_button(
                label=download_btn_text,
                data=zip_data,
                file_name=zip_filename,
                mime="application/zip",
                use_container_width=True,
                key="bot_dl"
            )

        except Exception as e:
            st.error(f"处理出错 (Error): {str(e)}")