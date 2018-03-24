#!/usr/bin/python
#-*- coding: utf-8 -*-
#encoding=utf-8

import urllib2
import urllib
import os
from BeautifulSoup import BeautifulSoup
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Referer': "http://www.mmjpg.com"
}

# 根据传入页码下载，默认下载首页，每页15
def downLoadAllImage(page=2):
    # html = urllib2.urlopen('http://www.mmjpg.com').read()
    req = urllib2.Request('http://www.mmjpg.com/home/%s' % page,headers=headers)
    html = urllib2.urlopen(req).read()
    # 解析html
    soup = BeautifulSoup(html)
    spanResult = soup.findAll('span',attrs={"class":"title"})

    for a in spanResult:
        name = a.find('a').string
        href = a.find('a').get('href')
        linkreq = urllib2.Request(href,headers=headers)
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
                print urlresult;
                request = urllib2.Request(urlresult, headers = headers)
                response = urllib2.urlopen(request)
                with open(filePath,"wb") as f:
                    f.write(response.read())


# 根据传入页码下载前n页，传5就是前5页 共n*15，默认1页即首页
def totalPage(page=1):

    for x in xrange(0,page):
        x += 1
        downLoadAllImage(x)



if __name__ == '__main__':

    downLoadAllImage(4)
    # totalPage(2)

