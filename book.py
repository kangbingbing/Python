#!/usr/bin/python
#-*- coding: utf-8 -*-
#encoding=utf-8
import urllib2
import urllib
from BeautifulSoup import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
 
if __name__ == '__main__':
    url = 'http://www.136book.com/mieyuechuanheji/'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html)
    divResult = soup.findAll('ol',attrs={"class":"clearfix"})

    print divResult
    for div in divResult:
        # 得到所有的a标签
        aarray = div.findAll('a')
        f = open('/Users/kangbing/Desktop/python/miyuezhuan.txt','w')
        for a in aarray:
            print a.string
            link = a.get('href')
            linkreq = urllib2.Request(link)
            linkresponse = urllib2.urlopen(linkreq)
            htmlres = linkresponse.read()
            soups = BeautifulSoup(htmlres)
            textResult = soups.findAll('div',attrs={"id":"content"})
            
            f.write(a.string)
            for p in textResult:
                parray = p.findAll('p')
                for string in parray:
                    f.write(string.string)
                    f.write('\n\n')
        f.close()




