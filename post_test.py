import requests
import base64

url = "http://127.0.0.1:20005/latex_rec"

image_page = "./public/screenshot-20231112-213530.png"
with open(image_page, "rb") as f:
    image_bytes = f.read()

data = {
    # "images": [
    #     base64.b64encode(image_bytes).decode("utf-8"),
    # ]*16 # 16 batch size
    "svgs": [
        "https://img.xkw.com/dksih/formula/5852c41e44d5d78bbcc3df98b5dc4a06.svg"
    ]*16 # 16 batch size
}

resp = requests.post(url, json=data)
if resp.status_code == 200:
    print(resp.json())
    for i in resp.json()["latex_texts"]:
        print(i)
