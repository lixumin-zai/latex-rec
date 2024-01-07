
#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import argparse
import re
import requests
from os import path
 
parser = argparse.ArgumentParser(description="svgtopng")
parser.add_argument("svgfilepath", default="./1.svg", help="The content of svgfile")
parser.add_argument("pngFileName", default="./1.png", help="The content of svgfile")
parser.add_argument("tempFilePath",default="/home/lixumin/project/xizhi_OCR/xizhi-latex-beta/temp", help="The content of svgfile")
args = parser.parse_args()
fileSavePath =args.tempFilePath
#读取SVG内容
headers = {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"}
response = requests.get(args.svgfilepath, headers=headers,timeout =4)
svgContent = response.content
svgContent = svgContent.decode("utf-8")
svgContent = svgContent.replace("\n","")
cairosvg.svg2png(url='https://img.xkw.com/dksih/formula/5852c41e44d5d78bbcc3df98b5dc4a06.svg', write_to='image.png', dpi=200, background_color='white', output_width=500, output_height=500)
cairosvg.svg2png(bytestring=data, write_to='image.png', dpi=200, background_color='white', output_width=500, output_height=200)

#写入到html中准备运行
code = '''
	<script type="module">
		var svgText = '%s'
		var domUrl = window.URL || window.webkitURL || window;
		if (!domUrl) {
			throw new Error("(browser doesnt support this)")
		}
		window.onload = async () => {
			var svg = new Blob([svgText], {
				type: "image/svg+xml;charset=utf-8"
			});
			var url = domUrl.createObjectURL(svg);
			document.write("<img src = '"+url+"'/>")
		}
	</script>
''' % svgContent
 
result3 = path.split(args.svgfilepath)
fileName = result3[1] +".html"
 
f = open(fileSavePath+"/"+fileName, "w")
f.write(code)
f.close()
 
#获取高度与宽度
matchObj = re.search( r'version=".*?" width="(.*?)px" height="(.*?)px"', svgContent, re.M|re.I)
 
# svgheight = matchObj.group(1)
# svgwidth = matchObj.group(2)
svgheight = 0.5
svgwidth = 0.5
print(4)
chrome_options = Options()
# chrome准备
# print(3)
# chrome_options.add_argument("--headless") # 无头模式
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--disable-dev-shm-usage')
print(2)
driver = webdriver.Chrome(options= chrome_options)
print(1)
driver.set_window_size(int(svgheight) +25, int(svgwidth)+20) # 25，20撑起窗口不显示水平条
driver.get("file:///"+fileSavePath+"/"+fileName)
imgFileName = fileSavePath + "/"+args.pngFileName+".png"
# 截图
driver.save_screenshot(imgFileName)
