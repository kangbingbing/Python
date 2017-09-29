#!/usr/bin/python
#-*- coding: utf-8 -*-
#encoding=utf-8

import urllib2
import urllib
import os
from BeautifulSoup import BeautifulSoup

# 根据传入页码下载，默认下载首页，每页15
def downLoadAllImage(page=1):
    # html = urllib2.urlopen('http://www.mmjpg.com').read()
    html = urllib2.urlopen('http://www.mmjpg.com/home/%s' % page).read()
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
        totalDiv = soups.find('div',attrs={'class':"page"})
        #  每套图的总数量
        aCount = totalDiv.findAll('a')[-2].string
        print aCount
        # print totalDiv

        for div in imageResult:
            # 得到所有的img标签
            image = div.find('img')
            # print image
            link = image.get('src')
            # print link
            # 拿到链接截取拼接
            for x in range(0,int(aCount)):
                x += 1
                urlresult = '%s%s%s' % (link[:-5], x, '.jpg')
                filePath = '/Users/kangbing/Desktop/image/%s%s.jpg' % (name,x)
                urllib.urlretrieve(urlresult,filePath)
                # print urlresult
                # print filePath.encode('utf-8')


# 根据传入页码下载前n页，传5就是前5页 共n*15，默认1页即首页
def totalPage(page=1):

    for x in xrange(0,page):
        x += 1
        downLoadAllImage(x)



if __name__ == '__main__':

    downLoadAllImage(1)
    # totalPage(2)

