#!/usr/bin/python
#-*- coding: utf-8 -*-
#encoding=utf-8

import xlwt
import xlrd
import xlutils.copy
import sys  
reload(sys)
import requests
import os
import json
import time

# 当前取的数组个数
currentCount = 0 
indexPage = 0 
pageCount = 50 


token = "2.00xYt9tCMvx9YBd9a4b97a83b4KB8D"
path = './souce/weibo.xls'

def read():
	
	data = xlrd.open_workbook(path)
	table = data.sheets()[0]       #通过索引顺序获取

	# 获取某一行的所有数据
	# print table.row_values(0)
	# 获取某一列的所有数据
	global array
	global currentCount

	array = table.col_values(18)
	del array[0]
	#  总量
	count = len(array)
	print count

	# 开始切割数组
	start = indexPage * pageCount
	end = (indexPage + 1) * pageCount
	if end > count:
		end = count


	tempArray = array[start : end]
	# print tempArray 
	currentCount = len(tempArray) 
	print '当前数组 %d 个' % currentCount 
	# 只取50个的 mid
	ids = ",".join(tempArray)
	print ids 
	# return
	idsStr = str(ids) 

	stateId(idsStr)



	# print array

def  stateId(x):

	values = {"mid":x,"type":"1","isBase62":"1","access_token":token,"is_batch":"1"}
	r = requests.get("https://api.weibo.com/2/statuses/queryid.json", params=values)
	results = r.json() 
	print results
	# print type(results)
	idArray = [] 
	for index in xrange(0, currentCount):
		dictR = results[index]
		key = array[index + indexPage * pageCount] 
		id_str = dictR[key] 
		# print id_str
		idArray.append(id_str) 

	# print idArray 
	weiboApi(idArray) 


def  weiboApi(idArray):
	##  把所有的 id 传进来
	ids = ",".join(idArray)
	# print ids 
	idsStr = str(ids) 
	# print idsStr
	print '---开始获取转评赞----'
	values = {"ids":idsStr,"access_token":token}
	r = requests.get("https://api.weibo.com/2/statuses/count.json", params=values)
	results = r.json() 
	print results
	print '---获取转评赞成功----'
	rb = xlrd.open_workbook(path)
	wb = xlutils.copy.copy(rb)
	#获取sheet对象，
	ws = wb.get_sheet(0)
	table = rb.sheets()[0]
	
	for x in xrange(0,currentCount):
		dictRes = results[x] 
		print dictRes 
		operationRow = (x + 1 + indexPage * pageCount)
		ws.write(operationRow, 8, dictRes['reposts'])
		ws.write(operationRow, 9, dictRes['comments'])
		ws.write(operationRow, 10, dictRes['attitudes'])
		ws.write(operationRow, 20, dictRes['id'])
		wb.save(path)
		print 'Excel索引%d  第%d行更改成功' % (operationRow, operationRow + 1) 

		if x == pageCount - 1:
			print "-------这一组最后一个了-----"
			global indexPage
			indexPage += 1 
			# time.sleep(1) 
			print "-------继续开始第%d页-----" % indexPage
			read() 
		

if __name__ == '__main__':
	read()