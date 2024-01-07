
from pydantic import BaseModel 
from typing import Union, List
from io import BytesIO
import base64
import time
import os
import aiohttp
import asyncio
import traceback

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
pretrained_model_name_or_path = f"./models/"

# init
model = VisionEncoderDecoderModel.from_pretrained(pretrained_model_name_or_path).to(device)
tokenizer = NougatTokenizerFast.from_pretrained(pretrained_model_name_or_path)
latex_processor = NougatLaTexProcessor.from_pretrained(pretrained_model_name_or_path)

# 异步get请求
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.read()


def norm_text(s: str):
    # 过滤
    s = s.replace("\,", " ")
    word = set(s)
    print(len(s)/len(word), len(s), len(word))
    # if len(word)/len(s) < 0.10:
    #     return "$ $"
    return s


class BatchUploadFile(BaseModel):
    images: List[str] = []
    svgs: List[str] = []

@apps.post("/latex_rec")
async def post_text_de(batch_upload_file: BatchUploadFile):
    # print(image)
    try:
        if batch_upload_file.images:
            images_bytes = []
            for image in batch_upload_file.images:
                image_bytes = base64.b64decode(image.encode("utf-8"))
                images_bytes.append(image_bytes)

        if batch_upload_file.svgs:
            images_bytes = []
            for svg in batch_upload_file.svgs:
                if svg.startswith("http"):
                    # svg是链接
                    async with aiohttp.ClientSession() as session:
                        svg_bytes = await fetch(session, svg)
                else:
                    svg_bytes = bytes(svg)
                image_bytes = cairosvg.svg2png(bytestring=svg_bytes, dpi=200, background_color='white', output_width=500, output_height=200)
                images_bytes.append(image_bytes)

    except Exception as e:
        traceback.print_exc()
        return {"code": 200 , "latex_texts": [], "error_msg": "输入不对"}

    item = []
    imgs = []
    for image_bytes in images_bytes:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        # 设置边框的颜色和大小
        border_color = (255, 255, 255)  # 白色边框
        border_size = 20  # 20 像素

        # 在图像周围添加边框
        image = ImageOps.expand(image, border=border_size, fill=border_color)
        imgs.append(image)
        if len(imgs) % 16 == 0:
            item.append(imgs)
            imgs = []
    if imgs:
        item.append(imgs)

    result = []
    for batch_imgs in item:
        pixel_values = latex_processor(batch_imgs, return_tensors="pt").pixel_values
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
            sequence = norm_text(sequence)
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
    pixel_values = latex_processor([image]*16, return_tensors="pt").pixel_values

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
    uvicorn.run("server:apps", host="0.0.0.0", port=20005, workers=3)

