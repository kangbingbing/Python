#!/usr/bin/python
#-*- coding: utf-8 -*-
#encoding=utf-8

import urllib2
import urllib
import os
from BeautifulSoup import BeautifulSoup

def downLoadAllImage():
    html = urllib2.urlopen('https://www.douban.com/photos/album/1652407753/').read()
    # 解析html
    soup = BeautifulSoup(html)
    # 从html里找到所有class 为 photo_wrap 的div
    divResult = soup.findAll('div',attrs={"class":"photo_wrap"})
    x = 0
    for div in divResult:
        # 得到所有的img标签
        imageArray = div.findAll('img')
        for image in imageArray:
            # 拿到img标签的链接
            link = image.get('src')
            # 拼接路径
            filePath = '/Users/kangbing/Desktop/images/%s.jpg' % x
            x += 1
            print filePath
            # 下载并保存到本地
            urllib.urlretrieve(link,filePath)
            print link

if __name__ == '__main__':
    downLoadAllImage()

