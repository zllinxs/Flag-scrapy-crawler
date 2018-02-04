# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os  
import urllib 
from Flag import settings

class FlagPipeline(object):
	def __init__(self):
		# 建立存储国名的文件
		self.f = open('nation_name.txt', 'w')
		
	def close_spider(self, spider):
		self.f.close()
		
	def process_item(self, item, spider):  
		dir_path = '%s/%s'%(settings.IMAGES_STORE, spider.name)#　国旗图片存储路径   
		if not os.path.exists(dir_path):  
			os.makedirs(dir_path)  
		image_url = item['flag']
		file_name = item['nation'] #　设置国名为图片名称   
		file_path = '%s/%s.png'%(dir_path,file_name)  
		if not os.path.exists(file_path):
			with open(file_path,'wb') as file_writer:
				conn = urllib.urlopen('http://example.webscraping.com' + str(image_url))#　根据flag的链接下载图片  
				file_writer.write(conn.read())  
			file_writer.close()  
		# 将国名存入f中
		self.f.write(file_name + '\t' + 'http://example.webscraping.com' + str(image_url) + '\n')
		return item  
