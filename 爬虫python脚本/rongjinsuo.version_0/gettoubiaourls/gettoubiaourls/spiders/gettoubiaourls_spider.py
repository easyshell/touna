#!/usr/bin/python
#-*-coding:utf-8-*-

import scrapy
from scrapy import Request
from gettoubiaourls.items import *
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
import os

class WeidaiSpider(scrapy.Spider):
	name = 'gettoubiaourls'
	start_urls = []
	handle_httpstatus_list = [301, 302, 400]

	def __init__(self):
		self.continuous_assign_date_limit = 10
		self.not_assign_date_count = 0
		self.assign_date = datetime.datetime.now().strftime("%Y-%m-%d")
		self.load_conf()
		self.rongdiya_base_url = "https://www.rjs.com/invest/diya/sort/asc/p/"
		self.rongxinyong_base_url = "https://www.rjs.com/invest/xy/sort/asc/p/"
		self.rongzulin_base_url = "https://www.rjs.com/invest/zl/sort/asc/p/"
		self.toubiao_base_url = "https://www.rjs.com/invest"
		self.page_num_record = codecs.open("page_num.record", "a+", "utf-8", errors="ignore")
	
	def __del__(self):
		self.page_num_record.close()
	
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
			if self.not_assign_date_count > self.continuous_assign_date_limit:
				return
			self.page_num_record.write(str(page_num) + "\n")
			rongdiya_url = self.rongdiya_base_url + str(page_num)
			rongxinyong_url = self.rongxinyong_base_url + str(page_num)
			rongzulin_url = self.rongzulin_base_url + str(page_num)
			yield scrapy.http.Request(url=rongdiya_url, callback=self.parse_rongdiya, meta={'product_classify':'rongdiya', 'page_num':page_num})
			yield scrapy.http.Request(url=rongxinyong_url, callback=self.parse_rongdiya, meta={'product_classify':'rongxinyong', 'page_num':page_num})
			yield scrapy.http.Request(url=rongzulin_url, callback=self.parse_rongdiya, meta={'product_classify':'rongzulin', 'page_num':page_num})

	def set_page_range(self, first_page, last_page):
		self.first_page = first_page
		self.last_page = last_page

	def parse_rongdiya(self, response):
		print("parse_roongdiya:" + response.url)
		hxs = HtmlXPathSelector(response)
		trs = hxs.select('/html/body/div[3]/div[4]/div[3]/table//tr').extract()
		url_item = GettoubiaourlsItem()
		
		for tr in trs:
			tr_sel = Selector(text=tr)
			href = tr_sel.xpath('//td/a[contains(@href, "/invest")]/@href').extract()
			date_of_invitation = tr_sel.xpath('//td[contains(@class, "resttime")]/strong/text()').extract()
			if len(href) > 0:
				toubiao_url = urlparse.urljoin(self.toubiao_base_url, href[0])
				date_of_invitation = date_of_invitation[0].strip()
				if date_of_invitation.find(self.assign_date) != -1:
					url_item['url'] = toubiao_url
					self.not_assign_date_count = 0
					yield url_item
				else:
					self.not_assign_date_count += 1
					if self.not_assign_date_count > self.continuous_assign_date_limit:
						return 
