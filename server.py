
from pydantic import BaseModel 
from typing import Union, List
from io import BytesIO
import base64
import time
import os
import re
import aiohttp
import asyncio
import traceback
import requests

from transformers import VisionEncoderDecoderModel
from transformers.models.nougat import NougatTokenizerFast

from fastapi import FastAPI, File
from PIL import Image, ImageOps
import numpy as np
import torch
import cv2
import cairosvg

from tools.util import process_raw_latex_code
from tools import NougatLaTexProcessor

apps = FastAPI()

# os.environ["CUDA_VISIBLE_DEVICES"] = "3" 
device = torch.device("cuda")
# file_dir = os.path.dirname(__file__)
# pretrained_model_name_or_path = f"{file_dir}/models/"
# pretrained_model_name_or_path = f"./models/"
pretrained_model_name_or_path = "/store/lixumin/xizhi_OCR/nougat_ocr/workspace/latex_ocr_mini_240130/"

# init
model = VisionEncoderDecoderModel.from_pretrained(pretrained_model_name_or_path).to(device)
tokenizer = NougatTokenizerFast.from_pretrained(pretrained_model_name_or_path)
latex_image_processor = NougatLaTexProcessor.from_pretrained(pretrained_model_name_or_path)

# 异步get请求
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.read()

# def filter_text(s: str) -> str:
#     # 过滤图片类识别
#     s = s.replace("\,", " ")
#     # if len(s) > 300: # 超过300个字符
#     #     word = set(s)
#     #     if len(word)/len(s) < 0.10:
#     #         # 重复的字符过多
#     #         return "$ $"
#     return s

def filter_text(s: str) -> str:
    # 过滤图片类识别
    if s.startswith("<smiles>"):
        return "$ $"
    # print(s)
    # print(re.match(r"^\$\s*\text{[\u4e00-\u9fa5a-zA-Z1-9\s]+}\s*\$$", s))
    if re.match(r"^\$\s*\\text{[\u4e00-\u9fa5a-zA-Z1-9\s]+}\s*\$$", s):
        # print(s)
        return "$ $"
    if len(s) > 300: # 超过300个字符
        s = s.replace("\,", " ")
        world = set(s)
        repeat_world = []
        for i in world:
            if s.count(i) > 30:
                # 重复的字符过多
                repeat_world.append(i)
        if len(repeat_world) > 0.5*len(world):
            return "$ $"
    return s

with open("/home/lixumin/project/xizhi_OCR/xizhi-latex-beta/public/84bcfb8295e7d975be5cab2e6b63793c89f589c593279a510c9e7fc7.png", "rb") as f:
    defaul_image_bytes = f.read()

def det_figure(image_bytes=None, image_url=None):
    url = "http://192.168.1.206:35000/figure-detect"
    if image_url:
        data = {
            "image_url": image_url,
        }
    if image_bytes:
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        data = {
            "image_base64": base64_image,
        }
    response = requests.post(url, json=data)
    picture_data = response.json()["data"]
    print(picture_data)
    return picture_data

class BatchUploadFile(BaseModel):
    images: List[str] = []
    svgs: List[str] = []

@apps.post("/latex_rec")
async def post_text_de(batch_upload_file: BatchUploadFile):
    # print(image)
    is_svg = []
    svg_process = False
    images_bytes = []
    try:
        if batch_upload_file.images:
            images_bytes = []
            for image in batch_upload_file.images:
                if image.startswith("http"):
                    try:
                        async with aiohttp.ClientSession() as session:
                            image_bytes = await fetch(session, image)
                    except:
                        image_bytes = None
                else:
                    image_bytes = base64.b64decode(image.encode("utf-8"))
                is_svg.append(0)
                images_bytes.append(image_bytes)


        if batch_upload_file.svgs:
            images_bytes = []
            for svg in batch_upload_file.svgs:
                if svg.startswith("http"):
                    # svg是链接
                    try:
                        async with aiohttp.ClientSession() as session:
                            svg_bytes = await fetch(session, svg)
                    except:
                        svg_bytes = None
                else:
                    svg_bytes = svg.encode('utf-8')
                if svg.startswith("http") and not svg.endswith(".svg"):
                    is_svg.append(0)
                    svg_process = True
                    images_bytes.append(svg_bytes)
                    continue
                else:
                    is_svg.append(1)
                output_height = 40 # 224
                # if len(re.findall(rb"<g(.*?)+</g>", svg_bytes)) - 1 > 6 :
                    # output_height = 100
                output_width = 560
                try:
                    image_bytes = cairosvg.svg2png(bytestring=svg_bytes, background_color='white')
                except:
                    image_bytes = b""
                    images_bytes.append(image_bytes)
                    continue
                image = Image.open(BytesIO(image_bytes)).convert("RGB")
                # print(len(re.findall(rb"<g(.*?)+</g>", svg_bytes)))
                # if len(re.findall(rb"<g(.*?)+</g>", svg_bytes)) - 1 <= 3:
                #     image_bytes = cairosvg.svg2png(bytestring=svg_bytes, dpi=200, background_color='white',output_height=output_height)
                #     image = Image.open(BytesIO(image_bytes)).convert("RGB")
                #     paste = Image.new("RGB", (image.size[0], image.size[1]+32), "white")
                #     paste.paste(image, (0, 16))
                #     with BytesIO() as byte_io:
                #         paste.save(byte_io, format='JPEG')  # or another format like PNG
                #         image_bytes = byte_io.getvalue()
                if image.size[1] > 34:
                    # 多行
                    output_height = 200
                    output_width = 1300
                    image_bytes = cairosvg.svg2png(bytestring=svg_bytes, dpi=200, background_color='white',
                        # output_width=output_width, 
                        output_height=output_height
                        )
                else:
                    image_bytes = cairosvg.svg2png(bytestring=svg_bytes, dpi=200, background_color='white',
                        # output_width=output_width, 
                        output_height=output_height
                        )
                # image_bytes = cairosvg.svg2png(
                #     bytestring=svg_bytes, 
                #     dpi=100, 
                #     background_color='white',
                #     scale=5)
                images_bytes.append(image_bytes)

    except Exception as e:
        traceback.print_exc()
        return {"code": 200 , "latex_texts": [], "error_msg": "输入不对"}

    item = []
    imgs = []
    for idx, image_bytes in enumerate(images_bytes):
        # print(image_bytes)
        if image_bytes:
            if not is_svg[idx] and svg_process:
                image = Image.open(BytesIO(image_bytes))
                if image.mode == "RGBA":
                        # 分离alpha通道
                    paste = Image.new("RGB", image.size, (255, 255, 255))
                    paste.paste(image, mask=image.split()[3])
                    image = paste
                bg_image = Image.new("RGB", (2*image.size[0], 2*image.size[1]), "white")
                bg_image.paste(image, (int(image.size[0]//2), int(image.size[1]//2)))
                # bg_image.save("./peitu.png")
                with BytesIO() as byte_io:
                    bg_image.save(byte_io, format='JPEG')  # or another format like PNG
                    image_bytes = byte_io.getvalue()
                if det_figure(image_bytes=image_bytes):
                    image = Image.open(BytesIO(defaul_image_bytes)).convert("RGB")
                    imgs.append(image)
                    continue
            image = Image.open(BytesIO(image_bytes)).convert("RGB")
            empty_img = Image.new("RGB", (image.size[0], image.size[1]+40), "white")
            image = Image.open(BytesIO(image_bytes)).convert("RGB")
            empty_img.paste(image, (0, 20))
            image = empty_img
            # 设置边框的颜色和大小
            border_color = (255, 255, 255)  # 白色边框
            border_size = 0  # 20 像素
        else:
            # print(1)
            image = Image.open(BytesIO(defaul_image_bytes)).convert("RGB")
            imgs.append(image)
        # # 在图像周围添加边框
        # image = ImageOps.expand(image, border=border_size, fill=border_color)
        # image.save("./show.jpg")
        
        imgs.append(image)
        if len(imgs) % 64 == 0:
            item.append(imgs)
            imgs = []
    if imgs:
        item.append(imgs)

    result = []
    for batch_imgs in item:
        pixel_values = latex_image_processor(batch_imgs, return_tensors="pt").pixel_values
        task_prompt = tokenizer.bos_token
        decoder_input_ids = tokenizer([task_prompt]*len(batch_imgs), add_special_tokens=False,
                                    return_tensors="pt").input_ids
        with torch.no_grad():
            outputs = model.generate(
                pixel_values.to(device),
                decoder_input_ids=decoder_input_ids.to(device),
                max_length=model.decoder.config.max_length,
                early_stopping=True,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
                use_cache=True,
                num_beams=1,
                bad_words_ids=[[tokenizer.unk_token_id]],
                return_dict_in_generate=True,
            )
        sequences = tokenizer.batch_decode(outputs.sequences)
        torch.cuda.empty_cache()
        for sequence in sequences:
            sequence = sequence.replace(tokenizer.eos_token, "").replace(tokenizer.pad_token, "").replace(tokenizer.bos_token,"")
            sequence = process_raw_latex_code(sequence)
            sequence = filter_text(sequence)
            result.append(sequence)
    
    return {"code": 200 , "latex_texts": result, "error_msg": ""}


class UploaFile(BaseModel):
    image: str

@apps.post("/latex_rec_1")
async def post_text_de(item: UploaFile):
    # print(image)
    image = item.image
    image_bytes = base64.b64decode(image.encode("utf-8"))
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    pixel_values = latex_image_processor([image]*16, return_tensors="pt").pixel_values

    task_prompt = tokenizer.bos_token
    decoder_input_ids = tokenizer([task_prompt]*16, add_special_tokens=False,
                                  return_tensors="pt").input_ids
    with torch.no_grad():
        outputs = model.generate(
            pixel_values.to(device),
            decoder_input_ids=decoder_input_ids.to(device),
            max_length=model.decoder.config.max_length,
            early_stopping=True,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
            use_cache=True,
            num_beams=1,
            bad_words_ids=[[tokenizer.unk_token_id]],
            return_dict_in_generate=True,
        )
    result = []
    sequences = tokenizer.batch_decode(outputs.sequences)
    for sequence in sequences:
        sequence = sequence.replace(tokenizer.eos_token, "").replace(tokenizer.pad_token, "").replace(tokenizer.bos_token,"")
        print(len(sequence))
        sequence = process_raw_latex_code(sequence)
        result.append(sequence)
    return {"latex_text": result}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("server:apps", host="0.0.0.0", port=20005, workers=1)

# {"svgs": [
#     "https://img.xkw.com/dksih/formula/dcec4050ad922c18239c38effcc45403.svg", 
#     "https://img.xkw.com/dksih/formula/73465a1f9aa03481295bf6bd3c6903ac.svg", 
#     "https://img.xkw.com/dksih/formula/e69d2b798744645af88a4fa411344a83.svg", 
#     "https://img.xkw.com/dksih/formula/fbea83c7be15a4e65147513673c9c63d.svg", 
#     "https://img.xkw.com/dksih/formula/4fe3a78950f6a4bb479c7ec0d8e57b5b.svg", 
#     "https://img.xkw.com/dksih/formula/e2fbe1b765f96cac84983c538ebb1fa2.svg", 
#     "https://img.xkw.com/dksih/formula/c15fb18163df0690365a0d2e7ee88f5a.svg", 
#     "https://img.xkw.com/dksih/formula/16828ef05d3f3aede894802ff40176b8.svg", 
#     "https://img.xkw.com/dksih/formula/b6ab74352a7c4e5cdf0b28b3847f1a9a.svg", 
#     "https://img.xkw.com/dksih/formula/462aecffea1ae3af482a6f65fe91e3a1.svg", 
#     "https://img.xkw.com/dksih/formula/65efbdf66f642e0dee3a097872e6186b.svg", 
#     "https://img.xkw.com/dksih/formula/735b2d327399f903f22d4a905a94bdda.svg", 
#     "https://img.xkw.com/dksih/formula/92550358311e5a353dbc03861a961a61.svg", 
#     "https://img.xkw.com/dksih/formula/6a533e6df135e50fa7282f2c1149a2cb.svg"]}