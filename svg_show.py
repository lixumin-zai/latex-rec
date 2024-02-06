import streamlit as st
from io import BytesIO
from PIL import Image
import base64
import requests
import json
import time
from streamlit_image_select import image_select

svg_list = [
    {"img_url":"https://img.xkw.com/dksih/formula/0c2df754f77604928c25690dde22b753.svg", "img_latex":r"$\mathrm{h}2$"},
    {"img_url":"https://img.xkw.com/dksih/formula/29c02d75ce4d63a88c298e139c24ad89.svg", "img_latex":r"$8x^{3}y^{2}:2x=$}"},
    {"img_url":"https://img.xkw.com/dksih/formula/e19cd21ee6300d3b21c748e7f79fc1ea.svg", "img_latex":r"$\begin{aligned}&\overrightarrow{O A}=\overrightarrow{O B}\end{aligned}$"},
    {"img_url":"https://img.xkw.com/dksih/formula/dc4876efa91f38d11ce12fed2e1fbf2e.svg", "img_latex":r"$\overline{O A}\perp\overline{O B}$"},
    {"img_url":"https://img.xkw.com/dksih/formula/2518948125c6adf678d84a78848b36aa.svg", "img_latex":r"$\begin{array}{|l|l|l|}\hline A\widehat{B}&=&A\widehat{C}&\end{array}$"},
    {"img_url":"https://img.xkw.com/dksih/formula/73e7cb9fda6686f7ce6c50f9c9d60c52.svg", "img_latex":r"$\overline{O C\mid A\bar{B}}$"},
    {"img_url":"https://img.xkw.com/dksih/formula/0c9b98022f4c279a271f49f3f69b24a6.svg", "img_latex":r"$A=\{y\mid y=2x+1,x\in R_{f}^{\},B=\{y\mid y=-x^{2},x\in R_{f}^{\}}$"},
    {"img_url":"https://img.xkw.com/dksih/formula/11bc05f41215f9894e11d1df0465751a.svg", "img_latex":r"$\mathrm{Y}$"},
    {"img_url":"https://img.xkw.com/dksih/formula/6563eb699f1bbc39eced661a2ebfcce4.svg", "img_latex":r"$\mathrm{Im}$"},
    {"img_url":"https://img.xkw.com/dksih/formula/819f22b85448181e7099d6218d93a972.svg", "img_latex":r"$\overline{A\bar{B}}\perp\overline{O C}$"}
]


with open("/home/lixumin/project/xizhi_OCR/xizhi-latex-beta/temp/data.json", "r") as f:
    svg_list = json.load(f)

for info in svg_list:
    with st.container():
        # 将第二个区域分成两列
        col1, col2 = st.columns(2)

        # 在第一列中显示图像
        col1.image(f"""{info['img_url']}""", caption="", width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

        # 在第二列中显示表格
        col2.markdown(rf"{info['img_latex']}")
    st.divider()

# col1, col2 = st.columns(2)
# # rows = st.rows(len(svg_list))
# with col1:
#     for idx, svg in enumerate(svg_list):
#         # with rows[idx]:
#         st.image(f"""{svg['img_url']}""", caption="", width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

# with col2:
#     for idx, latex in enumerate(svg_list):
#         # with rows[idx]:
#         st.markdown(rf"{latex['img_latex']}")
#             # st.image(f"""{}""", caption="", width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

# streamlit run svg_show.py