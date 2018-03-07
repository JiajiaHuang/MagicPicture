# -*- coding: utf-8 -*-
#========================================================
#
# @brief    多线程下载某关键字的百度图片
#
#========================================================
import requests
import urllib, urllib2
import threading, time
import os
import re


#正则匹配thumbURL链接
global g_regex
g_regex = re.compile(r'"thumbURL":"([^"]*)"')

#一页包含多少条数据
global g_pageContainNum
g_pageContainNum = 30

#要搜索的url
global g_url
g_url = 'https://image.baidu.com/search/acjson'


#模拟浏览器的header
global g_headers
g_headers = {
	"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
	"Accept": "text/plain"
}

#http://blog.csdn.net/qq_32166627/article/details/60882964
#========================================================
# @brief 多线程下载图片
# @params keyWord   在baidu那里搜索用到的关键字
#         startPage 从哪一页开始下载
#         endPage  结束页是哪张
#         savePath 图片保存的路径
#         preWord  图片保存的时候前缀(不如:abc)
#========================================================
def downloadPng(keyWord, startPage, endPage, savePath, preWord):
	global g_pageContainNum
	global g_regex
	global g_url
	global g_headers

	params = {
		"tn":"resultjson_com",
		"ipn":"rj",
		"ct":201326592,
		"is":"",
		"fp":"result",
		"queryWord":keyWord,#"怪诞小镇",
		"cl":2,
		"lm":-1,
		"ie":"utf-8",
		"oe":"utf-8",
		"adpicid":"",
		"st":"",
		"z":"",
		"ic":"",
		"word":keyWord,#"怪诞小镇",
		"s":"",
		"se":"",
		"tab":"",
		"width":"",
		"height":"",
		"face":"",
		"istype":"",
		"qc":"",
		"nc":1,
		"fr":"",
		#=========================================================
		#                  pn和rn是关键
		#  pn:下载哪一页(具体操作的时候会修改,比如0, 30, 60)
		#  rn:一页下载多少条数据的图片
		#=========================================================
		"pn":30,              
		"rn":g_pageContainNum,
		"gsm":78,
		"1519722930928":""
	}
	cnt = 1
	for index in range(startPage, endPage):
		#要下载哪一页
	 	pn = index*g_pageContainNum
	 	params["pn"] = pn
	 	#用urllib编码下参数
		decodeParams = urllib.urlencode(params)
		newUrl = g_url + "?" + decodeParams
		req = urllib2.Request(newUrl, headers=g_headers)
		page = urllib2.urlopen(req)
		#查找所有下载链接
		l = g_regex.findall(page.read())
		for picUrl in l:
			try:
				#下载图片
				pic = requests.get(picUrl, timeout=10)
			except requests.exceptions.ConnectionError:
				print("can not dowload:", picUrl)
				continue
			#保存图片
			f = open(savePath+"/"+preWord+str(index)+"_"+str(cnt)+".jpg", "wb");
			f.write(pic.content)
			f.close()
			cnt = cnt + 1
		# data = requests.get(url, params)#.json().get("data")
		

#========================================================
# @brief 多线程下载图片
# @params keyWord   在baidu那里搜索用到的关键字
#         totalPicNum 要下载的图片数量,因为按页去下载
#                     每一页30张，所有会按30的整倍数下载
#         savePath 图片保存的路径
#         preWord  图片保存的时候前缀(不如:abc)
# @example
#        multiThreadDownloadPic("怪诞小镇", 1000, "./gdxz_file_name", "gdxz_prename")
#========================================================
def multiThreadDownloadPic(keyWord, totalPicNum, savePath, preWord):
	global g_pageContainNum
	if not os.path.exists(savePath):
		os.mkdir(savePath)

	needPage = totalPicNum/g_pageContainNum
	if needPage*g_pageContainNum < totalPicNum:
		needPage = needPage + 1

	print("needPage:", needPage)

	#保存要等待的子线程
	waitForList = []
	#每两页开一条线程去执行
	for i in range(0, needPage, 2):
		t = threading.Thread(target=downloadPng, args=(keyWord, i, i+2, savePath, preWord))
		waitForList.append(t)
		t.start()
		#这里可以不sleep的,只是不想下载的太快所以才用的
		time.sleep(2)
	
	#这里要等待那些子线程退出,不然主线程退出了,
	#子线程还没完,会被结束掉
	for t in waitForList:
		t.join()
	print("exit main")



if "__main__" == __name__:
	# downloadPng("赵又廷", 0, 2, "./img", "")
	# downloadPng("怪诞小镇", 0, 2, "./img")
	# multiThreadDownloadPic("赵又廷三生三世剧照", 1000, "./img5", "ss")
	# multiThreadDownloadPic("赵又廷痞子英雄剧照", 1000, "./pzyx", "pzyx")
	# multiThreadDownloadPic("赵又廷艋舺", 1000, "./mj", "mj")
	# multiThreadDownloadPic("赵又廷致我们终将逝去的青春", 1000, "./zqc", "zqc")
	#下载怪诞小众
	multiThreadDownloadPic("怪诞小镇", 1000, "./gdxz_file_name", "gdxz_")
	# multiThreadDownloadPic("赵又廷", 1000, "./zyt", "zyt")
