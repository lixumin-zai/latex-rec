
```bash
docker build -t xizhi-latex-rec:0.0.1 .

docker run -dt --gpus all -p 30005:20005 -v ./temp:/exchange xizhi-latex-rec:0.0.1 bash 
```


```bash
apt install libcairo2-dev libjpeg-dev libgif-dev build-essential

```

```bash
CUDA_VISIBLE_DEVICES=3 python server.py
CUDA_VISIBLE_DEVICES=3 nohup python server.py > log.log &
CUDA_VISIBLE_DEVICES=3 nohup uvicorn server:apps --host 0.0.0.0 --port 20005 > log.log &
CUDA_VISIBLE_DEVICES=3 nohup uvicorn server:apps --host 0.0.0.0 --port 20005 --workers 3 > log.log &

```

```bash
streamlit run show_server.py
```