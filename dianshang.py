# coding:utf-8
from lxml import etree
import requests
import json
import os
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import MySQLdb

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
index = 0

class MysqlHelper:

    def __init__(self,host='localhost',port=3306,db='tiantian',user='root',passwd='123456',charset='utf8'):
        self.conn = MySQLdb.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)


    def insert(self,sql,params):
        return self.__cud(sql,params)


    def update(self,sql,params):
        return self.__cud(sql,params)


    def delete(self,sql,params):
        return self.__cud(sql,params)

    def __cud(self,sql,params=[]):
        try:
            cs1 = self.conn.cursor()
            rows = cs1.execute(sql, params)
            self.conn.commit()
            cs1.close()
            self.conn.close()
            return rows
        except Exception, e:
            print e
            self.conn.rollback()

    def fetchone(self, sql, params=[]):
        try:
            cs1 = self.conn.cursor()
            cs1.execute(sql, params)
            row = cs1.fetchone()
            cs1.close()
            self.conn.close()
            return row
        except Exception, e:
            print e

    def fetchall(self, sql, params=[]):
        try:
            cs1 = self.conn.cursor()
            cs1.execute(sql, params)
            rows = cs1.fetchall()
            cs1.close()
            self.conn.close()

            return rows
        except Exception, e:
            print e






def loadData():

    url = 'http://www.chunbo.com/'

    response = requests.get(url, headers=headers)
    html = response.text
    result = etree.HTML(html)

    # class包含article的  分类
    resultDiv = result.xpath("//a[@class='nav_all_lia all_site']")

    # 分类的banner图
    # 从第二张开始取, 第一张是热销
    categoryPics = result.xpath('//div[@class="one_pic"]/a[@class="cb-lazy-loading-bg"]/img')
    categoryPics.pop(0)
    categoryPics.pop(5)


    # 获取banner
    banners = result.xpath('//div[@class="banner_inner"]//a/@style')
    for banner in banners:
        banner_url = re.findall(r"\('(.*?)'\)", banner)[0]
        print(banner_url)

        banner_path = 'goods_img/banner/' + banner_url[-10:]
        if not os.path.exists("goods_img/banner/"):
            os.makedirs("goods_img/banner/")

        with open(banner_path, 'wb') as f:
            f.write(requests.get(banner_url).content)

        helper = MysqlHelper(db='tiantian')
        sql = 'insert into tt_goods_banner(banner_url,banner_pic) values(%s,%s)'
        helper.insert(sql, [banner_url,banner_path])


    for i in xrange(len(resultDiv)):
        item = resultDiv[i]
        link = item.xpath("./@href")[0]
        titleArray = item.xpath("./text()")
        title = "".join(titleArray).strip()
        print(title)
        print(link)

        # 取分类图片
        img = categoryPics[i]
        category_pic = img.xpath('./@data-original')[0]
        path = 'goods_img/' + title
        helper = MysqlHelper(db='tiantian')
        # 更新
        # sql = 'update tt_goods_goodstype set pic_path=%s,pic_url=%s where id=%s'
        # 插入
        sql = 'insert into tt_goods_goodstype(id,gtitle,isDelete,pic_path,pic_url) values(%s,%s,%s,%s,%s)'
        helper.insert(sql, [i+1,title,"0","",category_pic])

        if not os.path.exists(path):
            os.makedirs(path)

        # 取分类商品
        categoryPage(url=link,id=i+1,path=path)



def categoryPage(url,path,id,page=1):

    time.sleep(2.5)
    urls = url + "?page=" + str(page)
    response = requests.get(urls,headers=headers)
    html = response.text
    result = etree.HTML(html)
    print(result)
    items = result.xpath("//div[@class='shop_list']//li")
    pageCount = result.xpath("//div//a[@style='cursor:pointer']")
    print(items)


    for item in items:
        good_name = item.xpath("./h4/a/text()")[0]
        desc = "".join(item.xpath("./p[@class='name']/text()")).strip()
        price = item.xpath("./p/strong/text()")[0]
        unit = item.xpath("./p[@class='num']/text()")[0]
        pic = item.xpath("./a/img/@src")[0]
        item_id = item.xpath("//i/@data-pid")[0]
        price = price[2:]

        global index
        index += 1
        pic_name = path + '/' + str(index) + '.png'
        print(pic_name)
        helper = MysqlHelper(db='tiantian')
        sql = 'insert into tt_goods_goodsdetail(title,pic,price,isDelete,unit,clickCount,`desc`,stock,details,ad,goodsType_id,content) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        helper.insert(sql, [good_name,pic_name,float(price),"0",unit,100,desc,70,pic,'0',id,'html'])
        with open(pic_name, 'wb') as f:
            f.write(requests.get(pic).content)
        print('------')

    if len(pageCount) == page:
        print("最后一页了 已经结束")
    else:
        print("即将开始下一页")
        categoryPage(url,path=path,page=page+1,id=id)



if __name__ == '__main__':

    loadData()