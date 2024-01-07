
```bash
docker build -t xizhi-latex-rec:0.0.1 .

docker run -dt --gpus all -p 30005:20005 -v ./temp:/exchange xizhi-latex-rec:0.0.1 bash 
```


```bash
apt install libcairo2-dev libjpeg-dev libgif-dev build-essential

```