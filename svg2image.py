import cairosvg
from io import BytesIO
from PIL import Image, ImageOps
import re
import urllib
from urllib.request import urlopen

def svg2image():
    svg_bytes = b"""
    """


    # a = re.findall(rb"<g(.*?)+</g>", svg_bytes)
    # print(a)
    image_bytes = cairosvg.svg2png(bytestring=svg_bytes, dpi=200, background_color='white', 
                                    output_width=560, output_height=150, 
                                    scale=1)
    border_color = (255, 255, 255)  # 白色边框
    border_size = 0  # 20 像素
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    # 在图像周围添加边框
    image = ImageOps.expand(image, border=border_size, fill=border_color)
    image.save("./test.png")



def render_latex_to_image(tex):
    tex = urllib.parse.quote(tex, safe='')
    url = rf'https://www.zhihu.com/equation?tex={tex}'
    # html = urlopen(url).read().decode('utf-8').replace("font-size: 15px;","font-size: 15px;")
    html = urlopen(url).read()
    image_bytes = cairosvg.svg2png(bytestring=html, dpi=200, background_color='white', 
								output_width=560, output_height=150, 
								scale=1)
    with open("show.jpg", "wb") as f:
        f.write(image_bytes)
    # print(html)

tex = r"\mathbf{A}+\mathbf{B}=\left(\begin{array}{cccc}2+4&-1+7&3+(-8)\\0+9&4+3&6+5\\-6+1&10+(-1)&-5+2\end{array}\right)=\left(\begin{array}{rrrr}6&6&-5\\9&7&11\\-5&9&-3\end{array}\right)"
tex = r"\overrightarrow{O C}||\overrightarrow{A B}"
render_latex_to_image(tex)


