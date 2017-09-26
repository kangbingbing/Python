#!/usr/bin/python
#-*- coding: utf-8 -*-
#encoding=utf-8

import urllib2
import urllib
import os
from BeautifulSoup import BeautifulSoup

def downLoadAllImage():
    html = urllib2.urlopen('http://www.mmjpg.com').read()
    # 解析html
    soup = BeautifulSoup(html)
    spanResult = soup.findAll('span',attrs={"class":"title"})

    for a in spanResult:
        name = a.find('a').string
        href = a.find('a').get('href')
        linkreq = urllib2.Request(href)
        linkresponse = urllib2.urlopen(linkreq)
        htmlres = linkresponse.read()
        soups = BeautifulSoup(htmlres)
        imageResult = soups.findAll('div',attrs={"id":"content"})
        # print imageResult

        for div in imageResult:
            # 得到所有的img标签
            image = div.find('img')
            # print image
            link = image.get('src')
            # print link
            # 拿到链接截取拼接
            for x in range(1,41):
                urlresult = '%s%s%s' % (link[:-5], x, '.jpg')
                filePath = '/Users/kangbing/Desktop/image/%s%s.jpg' % (name,x)
                urllib.urlretrieve(urlresult,filePath)
                print urlresult
                print filePath.encode('utf-8')



if __name__ == '__main__':
    downLoadAllImage()

