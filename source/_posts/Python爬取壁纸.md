---
title: Python爬取壁纸
author: 5coder
tags:
  - 爬虫
  - 工具类
  - 壁纸
category: Python
abbrlink: 29206
date: 2022-08-28 13:47:34
password:
keywords:
top:
cover:
---

受害者网站：https://wallhaven.cc/ （是一个图片质量非常高的网站）

![](http://5coder.cn/img/1661665879_396422930e186e951632717cc73066c7.png)

直接上代码，复制粘贴就能用：

图片爬取

```python
import requests
import re
import os
import threading


def download(title, url):
    path = os.path.join('img', title)
    response = requests.get(url=url)
    with open(path, mode='wb') as f:
        f.write(response.content)


def getImg(start, end, th):
    for page in range(start, end):
        print('线程:', th, '---->第', page, '页')
        url = 'https://wallhaven.cc/toplist?page={}'.format(page)
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers)

        urls = re.findall('<a class="preview" href="(.*?)"', response.text)
        print(urls)
        for url in urls:
            with open('page_urls.txt', mode='a+') as f:
                f.write(url + "\n")
        for i in urls:
            response_2 = requests.get(url=i, headers=headers)
            img_url = re.findall('<img id="wallpaper" src="(.*?)"', response_2.text)[0]
            title = img_url.split('-')[-1]
            download(title, img_url)
            print(img_url)
            with open('img_urls.txt', mode='a+') as f:
                f.write(img_url)


if __name__ == '__main__':
    t1 = threading.Thread(target=getImg, args=(0, 100, 1))
    t2 = threading.Thread(target=getImg, args=(101, 200, 2))
    t3 = threading.Thread(target=getImg, args=(201, 300, 3))
    t1.start()
    t2.start()
    t3.start()

```

图片按照横版和竖版区分（将以下代码放在需要分隔的图片文件夹中运行）：

```python
# 横图竖图划分.py
import concurrent.futures as cf
from PIL import Image
import shutil
import time
import os
import re


class ImageClassfy(object):
    # 初始化
    def __init__(self):
        root = os.getcwd()  # 获取当前路径
        self.root = root
        self.names = os.listdir(root)
        self.widthImage = os.path.join(root, 'widthImage')
        self.heightImage = os.path.join(root, 'heightImage')
        self.count = 0
        self.pret()

    # 新建长图和宽度的保存文件夹
    def pret(self):
        for i in self.names:
            pattern = re.compile('(.png|.jpg)$')
            if not re.search(pattern, i):
                self.names.remove(i)
        self.sum = len(self.names)
        if not os.path.exists(self.widthImage):
            os.makedirs(self.widthImage)
        if not os.path.exists(self.heightImage):
            os.makedirs(self.heightImage)

    # 移动图片到对应的文件夹
    def move(self, name):
        src = os.path.join(self.root, name)
        img = Image.open(src)
        w, h = img.size
        img.close()
        if w >= h:
            shutil.move(src, self.widthImage)
        else:
            shutil.move(src, self.heightImage)

    # 打印进度条
    def show(self, num, _sum, runTime):
        barLen = 20  # 进度条的长度
        perFin = num / _sum
        numFin = round(barLen * perFin)
        numNon = barLen - numFin
        leftTime = (1 - perFin) * (runTime / perFin)
        print(
            f"{num:0>{len(str(_sum))}}/{_sum}",
            f"|{'█' * numFin}{' ' * numNon}|",
            f"任务进度: {perFin * 100:.2f}%",
            f"已用时间: {runTime:.2f}S",
            f"剩余时间: {leftTime:.2f}S",
            end='\r')
        if num == _sum:
            print()

    # 主函数
    def main(self):
        tp = cf.ThreadPoolExecutor(32)  # 多进程实现，指定进程数为32
        futures = []
        t1 = time.time()
        for name in self.names:
            future = tp.submit(self.move, name)
            futures.append(future)
        for future in cf.as_completed(futures):
            self.count += 1
            t2 = time.time()
            runTime = t2 - t1
            self.show(self.count, self.sum, runTime)
        tp.shutdown()


if __name__ == "__main__":
    ImageClassfy().main()
```

