#!/usr/bin/python
#-*-coding:utf-8-*-

import scrapy
from scrapy import Request
from shixin.items import *
from scrapy.selector import Selector
from scrapy.conf import settings
import requests
import urlparse
from bs4 import BeautifulSoup
import re
import ConfigParser
import sys
import time
from scrapy.selector import HtmlXPathSelector
import codecs
import sys
import datetime
import json

class ShixinSpider(scrapy.Spider):
	name = 'shixin'
	start_urls = []
	handle_httpstatus_list = [301, 302, 400]

	def __init__(self):
		self.load_conf()
		#self.url_base_prefix = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=%E5%85%A8%E5%9B%BD%E5%A4%B1%E4%BF%A1%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA%E5%90%8D%E5%8D%95&pn="
		self.url_base_prefix = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=%E5%A4%B1%E4%BF%A1%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA&pn="
		#self.url_base_sufix = "&rn=10&ie=utf-8&oe=utf-8&format=json&qq-pf-to=pcqq.temporaryc2c"
		self.url_base_sufix = "&rn=10&ie=utf-8&oe=utf-8&format=json&t=1470881717659&cb=jQuery110203868564622439057_1470880995693&_=1470880995778"
		
	def load_conf(self):
		conf = ConfigParser.ConfigParser()
		conf.read('con.ini')
		print("conf:")
		print(conf.sections())
		first_page = int(conf.get("range", "first_page"))
		last_page = int(conf.get("range", "last_page"))
		#last_page = 1
		self.set_page_range(first_page, last_page)

	def start_requests(self):
		for page_num in xrange(self.first_page, 1+self.last_page):
			self.shixin_zhixin_url = self.url_base_prefix + str(page_num*10) + self.url_base_sufix
			#print(self.shixin_zhixin_url)
			yield Request(url=self.shixin_zhixin_url, callback=self.parse_shixin_zhixin)

	def set_page_range(self, first_page, last_page):
		self.first_page = first_page
		self.last_page = last_page

	def parse_shixin_zhixin(self, response):
		shixin_info = ShixinItem()
		#print("parse_roongdiya:" + response.url)
		shixin_info['url'] = response.url
		shixin_info['body'] = response.body
		#print(type(shixin_info['body']))
		#print(response.body)
		yield shixin_info;
