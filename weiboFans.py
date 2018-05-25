# coding:utf-8

import urllib2
import urllib
import os
from BeautifulSoup import BeautifulSoup
import re
import xlwt
import xlrd
import xlutils.copy

start = 0
path = './souce/weibo.xls'

def readData():
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]  # 通过索引顺序获取
    array = table.col_values(17)
    
    wb = xlutils.copy.copy(data)
    # 获取sheet对象，
    ws = wb.get_sheet(0)
    del array[0]
    print '一共%d条数据' % (len(array))

    array = array[start: len(array)]
    print array
    # return

    for index in range(len(array)):

        uid = array[index]
        intuid = int(uid)
        uid = str(intuid)
        index1 = index + 1 + start
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
               'Cookie':'UOR=ent.ifeng.com,widget.weibo.com,ent.ifeng.com; SUB=_2AkMtoFKBf8NxqwJRmPkTyGvjb4p1ywzEieKb_KNaJRMxHRl-yT9kqlcdtRB6BiB8YLtx0aB4mPzIdAwtuebBchTSkQgR; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhN7r4HmKWHrs.HVfVcl5rK; _s_tentry=passport.weibo.com; Apache=3920561848700.257.1526521275000; SINAGLOBAL=3920561848700.257.1526521275000; ULV=1526521275109:1:1:1:3920561848700.257.1526521275000:; login_sid_t=b9f8e560734914165828b526d0438797; cross_origin_proto=SSL; YF-Page-G0=8ec35b246bb5b68c13549804abd380dc; YF-V5-G0=d45b2deaf680307fa1ec077ca90627d1'}
        url = 'https://www.weibo.com/u/' + uid
        print url
        req = urllib2.Request(url, headers=headers)
        try:
            html = urllib2.urlopen(req,timeout=5).read()
        except Exception as e:
            print '超时了'

            ws.write(index1, 7, u'超时了')
            wb.save(path)
            continue
            
        # 解析html
        soup = BeautifulSoup(html)
        spanResult = soup.findAll("script")

        for sc in spanResult:
            if sc.string.find(u'的粉丝(') != -1:
                # print sc.string
                # print repr(sc.string)
                # print re.findall('u4e1d\((.*?)\)<', repr(sc.string))
                array1 = re.findall('u4e1d\((.*?)\)<', repr(sc.string))
                value = int(array1[0])
                ws.write(index1, 13, value)
                wb.save(path)
                print '粉丝索引%d  第%d行更改成功 粉丝数[%d]个' % (index1-1, index1,value)

            if sc.string.find('icon_verify') != -1:
                ws.write(index1, 7, u'Y')
                wb.save(path)
                print '认证索引%d  第%d行更改成功  [已大V认证]' % (index1 - 1, index1)

        print '--------------------------------'


if __name__ == '__main__':

    readData()