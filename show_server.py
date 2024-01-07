import streamlit as st
from io import BytesIO
from PIL import Image
import base64
import requests
import json
import time
from streamlit_image_select import image_select

def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    return html
    # c = st.container()
    # c.write(html, unsafe_allow_html=True)

st.title("xizhi_latex_rec_beta")
st.divider() 
st.text("打印体公式识别，支持纯公式、英文+公式、多行公式。注意：多行文本会有漏识别情况.")
st.divider() 
example_image = image_select("example点击或上传图片:", [
        Image.open("./public/screenshot-20231112-213530.png").convert("RGB"),
        Image.open("./public/screenshot-20231113-095340.png").convert("RGB"),
        Image.open("./public/screenshot-20240107-104700.png").convert("RGB"),
        Image.open("./public/screenshot-20231127-092736.png").convert("RGB"),
        Image.open("./public/screenshot-20231229-235024.png").convert("RGB"),
    ]
)


uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"], accept_multiple_files=False)
st.caption('仅支持上传png、jpg、jpeg，svg使用API调用')

col1, col2 = st.columns(2)
# st.write(bytes_data)
url = "http://192.168.1.206:20005/latex_rec"

latex = ""
with col1:
    if example_image or uploaded_file:
        if example_image is not None:
            image = example_image
        if uploaded_file is not None:
            # if uploaded_file.type == "image/svg+xml":
            #     print(uploaded_file)
            #     html = render_svg(uploaded_file)
            # else:
            image = Image.open(uploaded_file)
            uploaded_file = None
        st.image(image, caption="上传的图片:", width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG') 
        data = {
            "images": [
                base64.b64encode(img_byte_arr.getvalue()).decode("utf-8")
            ]*1
        }
        tic = time.time()
        result = requests.post(url, json=data)
        toc = time.time()
        st.write(f"cost time:{toc-tic:05f}s")
        latex = result.json()["latex_texts"][0].replace("$", " $   ")
        example_image = None


with col2:
    if latex:
        print(latex)
        st.markdown(rf"{latex}")

if latex:
    st.text("识别的文本:")
    st.code(latex)
st.divider()
example_image = None


st.markdown(r"""```python
# 接口api
url = "http://192.168.1.206:20005/latex_rec"

# 参数定义
class BatchUploadFile(BaseModel):
    images: List[str] = []
    svgs: List[str] = []
```
""")
st.text("本地调用方法:")
st.markdown(r"""```python
import requests
import base64

url = "http://192.168.1.206:20005/latex_rec"

image_page = ""
with open(image_page, "rb") as f:
    image_bytes = f.read()

data = {
    # png jpg jpeg
    # "images": [
    #     base64.b64encode(image_bytes).decode("utf-8"),
    # ]*16 # 16 batch size
    # svg string/url
    "svgs": [
        "https://img.xkw.com/dksih/formula/5852c41e44d5d78bbcc3df98b5dc4a06.svg"
    ]*16 # 16 batch size
}
resp = requests.post(url, json=data)
if resp.status_code == 200:
    for i in resp.json()["latex_texts"]:
        print(i)
```
""")

# streamlit run show_server.py
# nohup streamlit run show_server.py > show.log
