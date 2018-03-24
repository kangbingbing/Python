#!/usr/bin/python
#-*- coding: utf-8 -*-
#encoding=utf-8

import urllib2
import urllib
import os
from BeautifulSoup import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}


def loadData(url,filedir):
    req = urllib2.Request(url,headers=headers)
    html = urllib2.urlopen(req).read()
    # 解析html
    soup = BeautifulSoup(html)

    presult = soup.findAll('p');
    # print presult;
    for plink in presult:

        img = plink.find('img');
        if img:
            imgurl = img.get('src')
            name = imgurl[-10:-4];
            # print imgurl
            if not imgurl.startswith('http'):
                imgurl = "http://www.bfpgf.com" + imgurl;
                
            filePath = '%s/%s.jpg' % (filedir,name)
            # print filePath;
            print imgurl;
            request = urllib2.Request(imgurl, None, headers)
            response = urllib2.urlopen(request)
            with open(filePath,"wb") as f:
                f.write(response.read())


# 某个主题总页数
def loadPage(url):

    req = urllib2.Request(url,headers=headers)
    html = urllib2.urlopen(req).read()
    # 解析html
    soup = BeautifulSoup(html)
    tilteRes = soup.title.string;
    print tilteRes;
    if tilteRes.find('/') != -1:
        index = tilteRes.find('/');
    else:
        index = tilteRes.index('-');

    filePath = '/Users/kangbing/Desktop/image1/%s' % (tilteRes[0:index]);
    print filePath;
    isExists = os.path.exists(filePath)

    if not isExists:
        os.makedirs(filePath) 
        pass
    else:
        print'文件夹已存在'
        return;


    spanResult = soup.findAll('div',attrs={"class":"article-paging"})
    print len(spanResult);
    # 一页直接下载, 多页一页一页下载
    if len(spanResult):
        for a in spanResult:
            for alink in a.findAll('a'):
                url = alink.get('href');
                # print url;
                # loadData(url,filePath);
    else:
        # loadData(url,filePath);
        # print url;
        pass

# 网站主页
def home(page=1):
    req = urllib2.Request(url='http://www.bfpgf.com/yld/page/%s' % page,headers=headers)
    html = urllib2.urlopen(req).read()
    # 解析html
    soup = BeautifulSoup(html)
    aresult = soup.findAll('a',attrs={"class":"thumbnail"})
    # print aresult;
    for alink in aresult:
        url = alink.get('href');
        loadPage(url)
        # print url;




if __name__ == '__main__':

    # 传入页数, 默认是1 , 每页10个主题
    home(1)



