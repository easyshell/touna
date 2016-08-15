# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
from gettoubiaourls.items import *
import datetime

class GettoubiaourlsPipeline(object):
	def __init__(self):
		now = datetime.datetime.now().strftime("%Y-%m-%d")
		self.urls_file = codecs.open("url_seeds/toubiao_urls.rongjinsuo." + now,  'a+', 'utf-8', errors='ignore')
	
	def __del__(self):
		self.urls_file.close()

	def process_item(self, item, spider):
		if isinstance(item, GettoubiaourlsItem):
			self.urls_file.write(item['url']+"\n")
					
