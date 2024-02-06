import requests
import base64
import time

url = "http://1.119.145.94:20005/latex_rec"

# image_page = "./public/screenshot-20231112-213530.png"
image_page = "./public/test1.jpeg"
with open(image_page, "rb") as f:
    image_bytes = f.read()

st = time.time()

data = {
    # "images": [
    #     "http://192.168.1.206:28700/screenshot-20240107-104700.png",
    #     # base64.b64encode(image_bytes).decode("utf-8"),
    # ]*1 # 16 batch size
    "svgs": [
        # "https://img.xkw.com/dksih/formula/4fe3a78950f6a4bb479c7ec0d8e57b5b.svg",
        "https://img.xkw.com/dksih/QBM/2017/11/30/1828555938103296/1830338482479104/EXPLANATION/264a5cb7492e4007a51839ce3c5c7e44.png",
        "https://img.xkw.com/dksih/QBM/2013/5/20/1573652606443520/1573652612497408/EXPLANATION/a3dd56120c4d45d2b888012a06aa60b6.png",

        # "https://img.xkw.com/dksih/QBM/editorImg/2023/6/28/94870bcb-059b-4153-ad3f-bc410238bb81.png",
        # "https://img.xkw.com/dksih/formula/86ebba6ed1add0fe647c0226614b9290.svg",
        # "https://img.xkw.com/dksih/formula/a09245fd7604997221b9a1a6e8fb752f.svg",
        # "http://192.168.1.206:28700/screenshot-20240107-104700.png",
        # "https://img.xkw.com/dksih/QBM/2018/10/23/2059733016125440/2067097506078720/STEM/0d9511ed1c8040df84c657af90918980.png",
        # "https://img.xkw.com/dksih/QBM/editorImg/2023/7/17/fba9fbaf-02ac-44ae-8a63-ac91df6b6efb.png",
        # "https://img.xkw.com/dksih/QBM/2019/5/13/2202888530673664/2203031944380416/EXPLANATION/1184ccc4a1b14f1a8218e11153d932ba.png",
        # "",

        # "https://img.xkw.com/dksih/formula/5852c41e44d5d78bbcc3df98b5dc4a06.svg"
        # "https://img.xkw.com/dksih/formula/d9347378165c36bb2e7a743cb1fd7f64.svg",
        # """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" stroke-dasharray="none" shape-rendering="auto" font-family="'Dialog'" width="30" text-rendering="auto" fill-opacity="1" contentScriptType="text/ecmascript" color-interpolation="auto" color-rendering="auto" preserveAspectRatio="xMidYMid meet" font-size="12" fill="black" stroke="black" image-rendering="auto" stroke-miterlimit="10" zoomAndPan="magnify" version="1.0" stroke-linecap="square" stroke-linejoin="miter" contentStyleType="text/css" font-style="normal" height="14" stroke-width="1" stroke-dashoffset="0" font-weight="normal" stroke-opacity="1"><defs id="genericDefs"/><g><g text-rendering="optimizeLegibility" transform="translate(0,13)" color-rendering="optimizeQuality" color-interpolation="linearRGB" image-rendering="optimizeQuality"><path d="M6.9531 -10.5938 L6.3438 -9.2656 L3.1562 -9.2656 L2.4531 -7.8438 Q4.5312 -7.5469 5.7344 -6.3125 Q6.7812 -5.25 6.7812 -3.8125 Q6.7812 -2.9688 6.4375 -2.2578 Q6.0938 -1.5469 5.5781 -1.0469 Q5.0625 -0.5469 4.4375 -0.25 Q3.5312 0.1875 2.5938 0.1875 Q1.6406 0.1875 1.2031 -0.1406 Q0.7656 -0.4688 0.7656 -0.8594 Q0.7656 -1.0781 0.9453 -1.2422 Q1.125 -1.4062 1.4062 -1.4062 Q1.6094 -1.4062 1.7578 -1.3438 Q1.9062 -1.2812 2.2812 -1.0312 Q2.8594 -0.625 3.4688 -0.625 Q4.375 -0.625 5.0703 -1.3125 Q5.7656 -2 5.7656 -3 Q5.7656 -3.9531 5.1484 -4.7891 Q4.5312 -5.625 3.4375 -6.0781 Q2.5938 -6.4219 1.125 -6.4844 L3.1562 -10.5938 L6.9531 -10.5938 ZM8.5781 -5.2344 Q8.5781 -7.0469 9.125 -8.3594 Q9.6719 -9.6719 10.5781 -10.3125 Q11.2812 -10.8125 12.0312 -10.8125 Q13.25 -10.8125 14.2188 -9.5781 Q15.4375 -8.0312 15.4375 -5.4062 Q15.4375 -3.5625 14.9062 -2.2734 Q14.375 -0.9844 13.5469 -0.3984 Q12.7188 0.1875 11.9531 0.1875 Q10.4375 0.1875 9.4375 -1.6094 Q8.5781 -3.1094 8.5781 -5.2344 ZM10.1094 -5.0469 Q10.1094 -2.8594 10.6562 -1.4688 Q11.0938 -0.3125 11.9844 -0.3125 Q12.4062 -0.3125 12.8594 -0.6875 Q13.3125 -1.0625 13.5469 -1.9531 Q13.9062 -3.2969 13.9062 -5.75 Q13.9062 -7.5625 13.5312 -8.7656 Q13.25 -9.6719 12.7969 -10.0469 Q12.4844 -10.2969 12.0312 -10.2969 Q11.5 -10.2969 11.0781 -9.8281 Q10.5156 -9.1719 10.3125 -7.7812 Q10.1094 -6.3906 10.1094 -5.0469 Z" stroke="none"/></g><g text-rendering="optimizeLegibility" transform="translate(15.4375,13)" color-rendering="optimizeQuality" color-interpolation="linearRGB" image-rendering="optimizeQuality"><path d="M4.5 -6.1562 Q3.2031 -6.1562 2.4531 -7.0078 Q1.7031 -7.8594 1.7031 -9.2188 Q1.7031 -10.6875 2.5 -11.5156 Q3.2969 -12.3438 4.5781 -12.3438 Q5.8438 -12.3438 6.5859 -11.5234 Q7.3281 -10.7031 7.3281 -9.2344 Q7.3281 -7.9219 6.5547 -7.0391 Q5.7812 -6.1562 4.5 -6.1562 ZM4.5625 -11.6406 Q3.5938 -11.6406 3.0312 -11 Q2.4688 -10.3594 2.4688 -9.2031 Q2.4688 -8.1094 3.0156 -7.4688 Q3.5625 -6.8281 4.5156 -6.8281 Q5.4688 -6.8281 6.0156 -7.4844 Q6.5625 -8.1406 6.5625 -9.25 Q6.5625 -10.4375 6.0234 -11.0391 Q5.4844 -11.6406 4.5625 -11.6406 ZM4.5156 0.2812 L3.6719 0.2812 L10.9531 -12.0938 L11.7656 -12.0938 L4.5156 0.2812 ZM11.1094 0.2188 Q9.8281 0.2188 9.0703 -0.6406 Q8.3125 -1.5 8.3125 -2.8594 Q8.3125 -4.3438 9.125 -5.1641 Q9.9375 -5.9844 11.2031 -5.9844 Q12.4688 -5.9844 13.2109 -5.1562 Q13.9531 -4.3281 13.9531 -2.875 Q13.9531 -1.5625 13.1797 -0.6719 Q12.4062 0.2188 11.1094 0.2188 ZM11.1719 -5.2969 Q10.2188 -5.2969 9.6562 -4.6406 Q9.0938 -3.9844 9.0938 -2.8438 Q9.0938 -1.75 9.6328 -1.1094 Q10.1719 -0.4688 11.125 -0.4688 Q12.0938 -0.4688 12.6406 -1.125 Q13.1875 -1.7812 13.1875 -2.8906 Q13.1875 -4.0781 12.6484 -4.6875 Q12.1094 -5.2969 11.1719 -5.2969 Z" stroke="none"/></g></g></svg>"""
        # """https://img.xkw.com/dksih/formula/c8468dfbf3b10346bc72cbc6456db997.svg""",
        # """https://img.xkw.com/dksih/formula/c29db8f7040703fd410a6fac67f24ebc.svg""",
        # """https://img.xkw.com/dksih/formula/14f4236b33ba75cf3197531babf3dd43.svg"""
    ]*1 # 16 batch size
}

# data = {
#     # "images": [
#     #     base64.b64encode(image_bytes).decode("utf-8"),
#     # ]*16 # 16 batch size
#     "svgs": [
#         "https://img.xkw.com/dksih/formula/7ee31829d0d4d5f779a957d7df8058ab.svg",
#         "https://img.xkw.com/dksih/formula/a6f7b16d65f1b2b8bea8cf4a83fde925.svg",
#         # "https://img.xkw.com/dksih/formula/87a60302649eb940748da818199e55da.svg",
#         # "https://img.xkw.com/dksih/formula/1292c47f62023b747f1a4bd615c75284.svg",
#         # "https://img.xkw.com/dksih/formula/d9347378165c36bb2e7a743cb1fd7f64.svg",
#         # "https://img.xkw.com/dksih/formula/5852c41e44d5d78bbcc3df98b5dc4a06.svg",
#         # """<?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE svg PUBLIC '-//W3C//DTD SVG 1.0//EN''http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd'><svg stroke-dasharray="none" shape-rendering="auto" xmlns="http://www.w3.org/2000/svg" font-family="&apos;Dialog&apos;" width="20" text-rendering="auto" fill-opacity="1" contentScriptType="text/ecmascript" color-interpolation="auto" color-rendering="auto" preserveAspectRatio="xMidYMid meet" font-size="12" fill="black" xmlns:xlink="http://www.w3.org/1999/xlink" stroke="black" image-rendering="auto" stroke-miterlimit="10" zoomAndPan="magnify" version="1.0" stroke-linecap="square" stroke-linejoin="miter" contentStyleType="text/css" font-style="normal" height="41" stroke-width="1" stroke-dashoffset="0" font-weight="normal" stroke-opacity="1"><!--Generated by the Batik Graphics2D SVG Generator--><defs id="genericDefs"/><g><g font-size="1" transform="scale(16,16) translate(0.37,0.8944)" text-rendering="geometricPrecision" color-rendering="optimizeQuality" image-rendering="optimizeQuality" font-family="&apos;jlm_cmr10&apos;" color-interpolation="linearRGB"><path d="M0.2969 -0.6406 L0.2969 -0.0781 Q0.2969 -0.0469 0.3125 -0.0469 Q0.3281 -0.0312 0.3906 -0.0312 L0.4219 -0.0312 L0.4219 0 Q0.3906 0 0.25 0 Q0.125 0 0.0938 0 L0.0938 -0.0312 L0.125 -0.0312 Q0.2031 -0.0312 0.2188 -0.0469 L0.2188 -0.0469 Q0.2188 -0.0625 0.2188 -0.0781 L0.2188 -0.5938 Q0.1719 -0.5781 0.0938 -0.5781 L0.0938 -0.6094 Q0.2031 -0.6094 0.2656 -0.6719 Q0.2969 -0.6719 0.2969 -0.6562 L0.2969 -0.6562 L0.2969 -0.6562 Q0.2969 -0.6562 0.2969 -0.6406 Z" stroke="none"/></g><g font-size="1" transform="matrix(16,0,0,16,0,0)" text-rendering="geometricPrecision" color-rendering="optimizeQuality" image-rendering="optimizeQuality" font-family="&apos;jlm_cmr10&apos;" color-interpolation="linearRGB"><rect x="0.37" width="0.5" height="0.04" y="1.301" stroke="none"/><path d="M0.4531 -0.1719 L0.4531 -0.1719 L0.4219 0 L0.0469 0 Q0.0469 -0.0312 0.0625 -0.0312 L0.0625 -0.0312 L0.25 -0.25 Q0.3594 -0.375 0.3594 -0.4688 Q0.3594 -0.5625 0.2969 -0.6094 L0.2969 -0.6094 L0.2969 -0.6094 Q0.2656 -0.6406 0.2188 -0.6406 Q0.1562 -0.6406 0.1094 -0.5781 Q0.0938 -0.5625 0.0938 -0.5312 Q0.0938 -0.5312 0.1094 -0.5312 Q0.1406 -0.5312 0.1562 -0.5 L0.1562 -0.5 Q0.1562 -0.4844 0.1562 -0.4844 Q0.1562 -0.4375 0.1094 -0.4375 Q0.1094 -0.4219 0.1094 -0.4219 Q0.0625 -0.4219 0.0469 -0.4531 Q0.0469 -0.4688 0.0469 -0.4844 Q0.0469 -0.5625 0.1094 -0.6094 Q0.1562 -0.6719 0.2344 -0.6719 Q0.3438 -0.6719 0.4062 -0.5938 Q0.4375 -0.5469 0.4531 -0.4844 Q0.4531 -0.4844 0.4531 -0.4688 Q0.4531 -0.4062 0.3906 -0.3281 Q0.3594 -0.2969 0.2969 -0.25 L0.25 -0.1875 L0.2344 -0.1875 L0.125 -0.0781 L0.3125 -0.0781 Q0.3906 -0.0781 0.4062 -0.0781 Q0.4062 -0.0938 0.4219 -0.1719 L0.4531 -0.1719 Z" transform="translate(0.37,2.2569)" stroke="none"/></g></g></svg>"""
#     ]*64 # 16 batch size
# }

resp = requests.post(url, json=data)
print(resp.text)
if resp.status_code == 200:
    print(resp.json())
    for i in resp.json()["latex_texts"]:
        print(i)

print(time.time()-st)