FROM ubuntu:20.04

WORKDIR /work

COPY . /work

# 更改软件源为阿里云
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    apt-get update

RUN apt-get update && \
    apt-get install -y git gcc python3-pip && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y libffi-dev libcairo2-dev libjpeg-dev libgif-dev build-essential && \
    pip3 install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 -i https://mirror.baidu.com/pypi/simple && \
    pip3 install --no-cache-dir -r requirements.txt -i https://mirror.baidu.com/pypi/simple && \
    pip3 uninstall opencv-python -y && \
    pip3 install opencv-python-headless==4.8.0.74 -i https://mirror.baidu.com/pypi/simple 

# 开放端口
EXPOSE 20005

