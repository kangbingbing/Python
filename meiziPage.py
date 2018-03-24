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
			print imgurl
			filePath = '%s/%s.jpg' % (filedir,name)
			request = urllib2.Request(imgurl, None, headers)
			response = urllib2.urlopen(request)
			with open(filePath,"wb") as f:
				f.write(response.read())


# 某个主题总页数
def loadPage():

	req = urllib2.Request(url='http://www.bfpgf.com/yld/72578.html',headers=headers)
	html = urllib2.urlopen(req).read()
	# 解析html
	soup = BeautifulSoup(html)
	tilteRes = soup.title.string;
	index = tilteRes.index('-');
	filePath = '/Users/kangbing/Desktop/image/%s' % (tilteRes[0:index]);
	print filePath;
	isExists = os.path.exists(filePath)

	if not isExists:
		os.makedirs(filePath) 
	else:
		print'文件夹已存在'

	spanResult = soup.findAll('div',attrs={"class":"article-paging"})
	# print spanResult;
	for a in spanResult:
		for alink in a.findAll('a'):
			url = alink.get('href');
			print url;
			loadData(url,filePath);


if __name__ == '__main__':

    loadPage()


