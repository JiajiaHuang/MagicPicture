# -*- coding: utf-8 -*-

from PIL import Image
import os
import shutil
import urllib
import random


global g_iconWidth
g_iconWidth = 36


#========================================================
# @brief 计算一小块区域的平均颜色值
# @params dataList       正张图的数据
#         col, row       起始位置,多少列,多少行
#         width,height   整张图的宽高
#         stepWidth      这一小块正方形的边长是多少
# @example
#          **********
#          ***XXX****
#          ***XXX****
#          ***XXX****
#          **********
#          算XXX那的平均值,(dataList, 3, 1, 10, 5, 3)
#========================================================
def caculateOneRangeAvgValue(dataList, col, row, width, height, stepWidth):
	r = 0
	g = 0
	b = 0
	cnt = 0
	length = len(dataList)
	for _row in range(0, stepWidth):
		for _col in range(0, stepWidth):
			newRow = row + _row
			newCol = col + _col
			if newRow*width+newCol < length:
				cnt = cnt + 1
				rgb = dataList[newRow*width+newCol]
				r += rgb[0]
				g += rgb[1]
				b += rgb[2]
				
	# return (r/9, g/9, b/9)
	return (r/cnt, g/cnt, b/cnt)

#========================================================
# @brief 计算整张图的平均颜色值
#========================================================
def caculateAvgValue(im):
	dataList = list(im.getdata())
	r = 0
	g = 0
	b = 0
	length = len(dataList)
	for rgb in dataList:
		r += rgb[0]
		g += rgb[1]
		b += rgb[2]
	return (r/length, g/length, b/length)

#========================================================
# @brief 调整图片的大小
#        长方形的图片统一裁剪成正方形
# @return 返回两张图片
#         1张图标icon
#         1张用来计算颜色值的
#========================================================
# def reSizePic(im, width, height):
def reSizePic(im):
	global g_iconWidth
	width = im.size[0]
	height = im.size[1]
	#最短边为正方形的边长
	w = height
	if width < height:
		w = width
	#这里除以5乘以4只是为了更加精确凸出图片
	#的主颜色(一般都是中间嘛)
	w = w/5*4
	#裁剪中间区域
	l = (width-w)/2
	up = (height-w)/2
	standerIm = im.crop((l, up, l+w, up+w))
	
	return standerIm.resize((g_iconWidth, g_iconWidth), Image.ANTIALIAS), \
			standerIm.resize((9, 9), Image.ANTIALIAS)


#========================================================
# @brief 计算单张图片,并生成图标
#        
# @params pngPath    图片的路径
#         fileName   图片名
#         targetPath 保存的路径
#========================================================
def caculateOnePngAndGenerateRPGIcon(pngPath, fileName, targetPath):
	im = Image.open(pngPath+"/"+fileName).convert("RGB");
	iconIm, newIm = reSizePic(im)
	value = caculateAvgValue(newIm)
	print("avg value:", value)
	iconIm.save(targetPath+"/"+str(value[0])+"_"+str(value[1])+"_"+str(value[2])+".png")



#========================================================
# @brief 获取颜色值相近的图片
# @params value       颜色值
#         iconRgbList 查找的rgb列表
#========================================================
def dealWithImageFile(srcPath, desPath, iconGeneratePath):
	if not os.path.exists(srcPath):
		os.mkdir(srcPath)

	if not os.path.exists(desPath):
		os.mkdir(desPath)

	if not os.path.exists(iconGeneratePath):
		os.mkdir(iconGeneratePath)

	l = os.listdir(srcPath)

	for fileName in l:
		caculateOnePngAndGenerateRPGIcon(srcPath, fileName, iconGeneratePath)
		shutil.move(srcPath+"/"+fileName, desPath+"/"+fileName)


#========================================================
# @brief 获取颜色值相近的图片
# @params value       颜色值
#         iconRgbList 查找的rgb列表
#========================================================
def findNearestIcon(value, iconRgbList):
	dis = 123456
	nearestRgb = None
	r = value[0]
	g = value[1]
	b = value[2]
	for rgb in iconRgbList:
		curDis = abs(rgb[0]-r) + abs(rgb[1]-g) + abs(rgb[2]-b)
		if curDis < dis:
			dis = curDis
			nearestRgb = rgb
	return str(nearestRgb[0])+"_"+str(nearestRgb[1])+"_"+str(nearestRgb[2])+".png"

# global mapHaveUseIcon
# mapHaveUseIcon = {}
# def findNearestIcon(value, iconRgbList):
# 	global mapHaveUseIcon
# 	dis = 123456
# 	nearestRgb = None
# 	r = value[0]
# 	g = value[1]
# 	b = value[2]
# 	nearestList = []
# 	for rgb in iconRgbList:
# 		curDis = abs(rgb[0]-r) + abs(rgb[1]-g) + abs(rgb[2]-b)
# 		if curDis < dis:
# 			dis = curDis
# 			nearestRgb = rgb
# 			nearestList.append(rgb)

# 	length = len(nearestList)
# 	if length>=3:
# 		findIt = False
# 		for index in range(length, 0, -1):
# 			if False == mapHaveUseIcon.has_key(str(nearestList[index-1])):
# 				nearestRgb = nearestList[index-1]
# 				findIt = True
# 				break
# 		if False == findIt:
# 			nearestRgb = nearestList[random.randint(length-4, length-1)]

# 	mapHaveUseIcon[str(nearestRgb)] = True
# 	# global i
# 	# if i <= 5:
# 	# 	print("length:", length)
# 	# 	i = i + 1
# 	# 	for rgb in nearestList:
# 	# 		curDis = abs(rgb[0]-r) + abs(rgb[1]-g) + abs(rgb[2]-b)
# 	# 		print(curDis)

# 	return str(nearestRgb[0])+"_"+str(nearestRgb[1])+"_"+str(nearestRgb[2])+".png"


#========================================================
# @brief 获取所有图标的RGB值
# @params iconPath      图标目录
#========================================================
def getIconRgbList(iconPath):
	l = os.listdir(iconPath)
	iconRgbList = []
	for name in l:
		rgb = name[:-4].split("_")
		iconRgbList.append((int(rgb[0]), int(rgb[1]), int(rgb[2])))
	return iconRgbList


#========================================================
# @brief 生成图片
# @params iconPath      图标目录
#         targetPath    目标路径
#         targetPicName 目标图片名(就是要生成哪张图片)
#========================================================
def generatePic(iconPath, targetPath, targetPicName):
	global g_iconWidth

	iconRgbList = getIconRgbList(iconPath)

	tIm = Image.open(targetPath+"/"+targetPicName).convert("RGB");
	w = tIm.size[0]
	h = tIm.size[1]
	print("w, h:", w, h)

	targetDataList = list(tIm.getdata())
	stepWidth = 3

	multiPly = g_iconWidth/stepWidth
	# multiPly = 36/stepWidth
	newIm = Image.new("RGB", (w*multiPly, h*multiPly), "white")


	for col in range(0, w, stepWidth):
		for row in range(0, h, stepWidth):
			value = caculateOneRangeAvgValue(targetDataList, col, row, w, h, stepWidth)
			iconName = findNearestIcon(value, iconRgbList)
			iconIm = Image.open(iconPath+"/"+iconName).copy()
			# iconIm = iconIm.resize((36, 36), Image.ANTIALIAS).copy()
			newIm.paste(iconIm, (col*multiPly, row*multiPly))

	newIm.save(targetPath+"/"+"new_"+targetPicName)


if __name__ == "__main__":
	dealWithImageFile("./src_img", "./des_img", "./icon3_img")
	# generatePic("./icon_img", "./", "timg.jpg")
	# generatePic("./icon2_img", "./", "beibei.jpg")