#!/usr/bin/python
#-*-coding:utf-8-*-

import scrapy
from scrapy import Request
from rongjinsuo.items import *
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

class WeidaiSpider(scrapy.Spider):
	name = 'rongjinsuo'
	start_urls = []
	handle_httpstatus_list = [301, 302, 400]

	def __init__(self):
		self.load_conf()
		self.rongdiya_base_url = "https://www.rjs.com/invest/diya/sort/asc/p/"
		self.rongxinyong_base_url = "https://www.rjs.com/invest/xy/sort/asc/p/"
		self.rongzulin_base_url = "https://www.rjs.com/invest/zl/sort/asc/p/"	
		self.rongdiya_toubiao_base_url = "https://www.rjs.com/invest"
	
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
		for page_num in range(self.first_page, 1+self.last_page):
			#print(page_num)
			rongdiya_url = self.rongdiya_base_url + str(page_num)
			rongxinyong_url = self.rongxinyong_base_url + str(page_num)
			rongzulin_url = self.rongzulin_base_url + str(page_num)
			
			#because toubiao of rongdiya and rongxinyong and rongzulin in location of html web is the same, so they common to use method 'parse_rongdiya'
			
			yield scrapy.http.Request(url=rongdiya_url, callback=self.parse_rongdiya, meta={'product_classify':'rongdiya'})
			yield scrapy.http.Request(url=rongxinyong_url, callback=self.parse_rongdiya, meta={'product_classify':'rongxinyong'})
			yield scrapy.http.Request(url=rongzulin_url, callback=self.parse_rongdiya, meta={'product_classify':'rongzulin'})

	def set_page_range(self, first_page, last_page):
		self.first_page = first_page
		self.last_page = last_page

	def parse_rongdiya(self, response):
		print("parse_roongdiya:" + response.url)
		hxs = HtmlXPathSelector(response)
		hrefs = hxs.select('/html/body/div[3]/div[4]/div[3]/table//tr/td/a[contains(@href, "/invest")]/@href').extract()
		#print(hrefs)
		for href in hrefs:
			if re.compile(r"html").search(href):
					rongdiya_toubiao_url = urlparse.urljoin(self.rongdiya_base_url, href)
					#print(rongdiya_toubiao_url)
					yield Request(url=rongdiya_toubiao_url, callback=self.parse_rongdiya_toubiao, meta=response.meta)
	
	def parse_rongdiya_toubiao(self, response):
		print("parse_rongdiya_toubiao" + response.url)
		sel = Selector(text=response.body_as_unicode())
		rongdiya_info = RongJinSuoItem()
		rongdiya_info['product_classify'] = response.meta['product_classify'].decode('ascii')
		#print(rongdiya_info['product_classify'])
		rongdiya_info['url'] = response.url.decode('ascii')
		rongdiya_info['title'] = sel.xpath('/html/body/div[3]/div[4]/div[1]/div[1]/h1/text()').extract()[0]
		#print(rongdiya_info['title'].encode('utf-8'))
		rongdiya_info['expected_annual_income'] = sel.xpath('/html/body/div[3]/div[4]/div[1]/div[2]/table//tr/td[1]/div/h4/text()').extract()[0]
		#print(rongdiya_info['expected_annual_income'].encode('utf-8'))
		rongdiya_info['lock_time'] = sel.xpath('/html/body/div[3]/div[4]/div[1]/div[2]/table//tr/td[2]/div/h4/text()').extract()[0]
		#print(rongdiya_info['lock_time'].encode('utf-8'))
		rongdiya_info['project_amount'] = sel.xpath('/html/body/div[3]/div[4]/div[1]/div[3]/div[1]/table//tr[1]/td[1]/text()').extract()[0]
		#print(rongdiya_info['project_amount'].encode('utf-8'))
		rongdiya_info['project_number'] = sel.xpath('/html/body/div[3]/div[4]/div[1]/div[3]/div[1]/table//tr[1]/td[2]/text()').extract()[0]
		#print(rongdiya_info['project_number'].encode('utf-8'))
		rongdiya_info['repay_method'] = sel.xpath('/html/body/div[3]/div[4]/div[1]/div[3]/div[1]/table//tr[1]/td[3]/text()').extract()[0]
		#print(rongdiya_info['repay_method'].encode('utf-8'))
		rongdiya_info['use_of_funds'] = sel.xpath('/html/body/div[3]/div[4]/div[1]/div[3]/div[1]/table//tr[2]/td[1]/text()').extract()[0]	
		#print(rongdiya_info['use_of_funds'].encode('utf-8'))
		rongdiya_info['product_provide'] = sel.xpath('/html/body/div[3]/div[4]/div[1]/div[3]/div[1]/table//tr[3]/td[2]/a/text()').extract()[0]
		#print(rongdiya_info['product_provide'].encode('utf-8'))
		rongdiya_info['date_of_invitation'] = sel.xpath('/html/body/div[3]/div[4]/div[1]/div[3]/div[1]/table//tr[3]/td[3]/strong/text()').extract()[0]
		#print(rongdiya_info['date_of_invitation'].encode('utf-8'))
		rongdiya_info['completion'] = sel.xpath('/html/body/div[3]/div[4]/div[1]/div[4]/div[1]/div/p/text()').extract()[0]
		#print(rongdiya_info['completion'].encode('utf-8'))
		rongdiya_info['car_models'] = sel.xpath('/html/body/div[3]/div[4]/div[2]/div[1]/ul/li[1]/text()').extract()[0]
		#print(rongdiya_info['car_models'].encode('utf-8'))
		try:
			rongdiya_info['evaluating_price'] = sel.xpath('/html/body/div[3]/div[4]/div[2]/div[1]/ul/li[2]/text()').extract()[0]
			#print(rongdiya_info['evaluating_price'].encode('utf-8'))
		except IndexError:
			rongdiya_info['evaluating_price'] = u""
			print("evaluating_price index error")
	
		try:
			rongdiya_info['record_date'] = sel.xpath('/html/body/div[3]/div[4]/div[2]/div[1]/ul/li[3]/text()').extract()[0]
			#print(rongdiya_info['record_date'].encode('utf-8'))
		except IndexError:
			rongdiya_info['record_date'] = u""
			print("record_date index error")
		
		try:
			rongdiya_info['xinghao'] = sel.xpath('/html/body/div[3]/div[4]/div[2]/div[1]/ul/li[4]/text()').extract()[0]
			#print(rongdiya_info['xinghao'].encode('utf-8'))
		except IndexError:
			rongdiya_info['xinghao'] = u""
			print("xinghao index error")
		
		try:
			rongdiya_info['appraiser'] = sel.xpath('//*[@id="int"]/p/a/text()').extract()[0]
			#print(rongdiya_info['appraiser'].encode('utf-8'))
		except IndexError:
			rongdiya_info['appraiser'] = u""
			print("appraiser index error")
		
		try:
			rongdiya_info['borrower'] = sel.xpath('/html/body/div[3]/div[4]/div[2]/div[2]/div[1]/dl/dt/text()').extract()[0]
			#print(rongdiya_info['borrower'].encode('utf-8'))
		except IndexError:
			rongdiya_info['borrower'] = u""
			print("borrower index error")
		
		rongdiya_info['credit_rating'] = sel.xpath('/html/body/div[3]/div[4]/div[2]/div[2]/div[1]/dl/dd/a/div/text()').extract()[0]
		#print(rongdiya_info['credit_rating'].encode('utf-8'))
		try:
			rongdiya_info['gender'] = sel.xpath('/html/body/div[3]/div[4]/div[2]/div[2]/div[2]/table//tr[1]/td[1]/text()').extract()[0]
			#print(rongdiya_info['gender'].encode('utf-8'))
		except IndexError:
			rongdiya_info['gender'] = u""
			print("gender index error")
		
		try:	
			rongdiya_info['mariage'] = sel.xpath('/html/body/div[3]/div[4]/div[2]/div[2]/div[2]/table//tr[2]/td[1]/text()').extract()[0]
			#print(rongdiya_info['mariage'].encode('utf-8'))
		except IndexError:
			rongdiya_info['mariage'] = u""
			print("mariage index error")
		
		try:
			rongdiya_info['education'] = sel.xpath('/html/body/div[3]/div[4]/div[2]/div[2]/div[2]/table//tr[3]/td[1]/text()').extract()[0]
			#print(rongdiya_info['education'].encode('utf-8'))
		except IndexError:
			rongdiya_info['education'] = u""
			print("education index error")
		
		try:
			rongdiya_info['borrowing_type'] = sel.xpath('/html/body/div[3]/div[4]/div[2]/div[2]/div[2]/table//tr[4]/td[1]/text()').extract()[0]
			#print(rongdiya_info['borrowing_type'].encode('utf-8'))
		except IndexError:
			rongdiya_info['borrowing_type'] = u""
			print("borrowing_type index error")
		
		try:
			rongdiya_info['id_number'] = sel.xpath('/html/body/div[3]/div[4]/div[2]/div[2]/div[2]/table//tr[5]/td[1]/text()').extract()[0]
			#print(rongdiya_info['id_number'].encode('utf-8'))
		except IndexError:
			rongdiya_info['id_number'] = u""
			print("id_number index error")
		
		try:	
			rongdiya_info['age'] = sel.xpath('/html/body/div[3]/div[4]/div[2]/div[2]/div[2]/table//tr[1]/td[2]/text()').extract()[0]
			#print(rongdiya_info['age'].encode('utf-8'))
		except IndexError:
			rongdiya_info['age'] = u""
			print("age index error")
		
		try:
			rongdiya_info['working_year'] = sel.xpath('/html/body/div[3]/div[4]/div[2]/div[2]/div[2]/table//tr[2]/td[2]/text()').extract()[0]
			#print(rongdiya_info['working_year'].encode('utf-8'))
		except IndexError:
			rongdiya_info['working_year'] = u""
			print("working_year index error")
		
		try:	
			rongdiya_info['present_address'] = sel.xpath('/html/body/div[3]/div[4]/div[2]/div[2]/div[2]/table//tr[3]/td[2]/text()').extract()[0]
			#print(rongdiya_info['present_address'].encode('utf-8'))
		except IndexError:
			rongdiya_info['present_address'] = u""
			print("present_address index error")
		
		try:
			rongdiya_info['native_place'] = sel.xpath('/html/body/div[3]/div[4]/div[2]/div[2]/div[2]/table//tr[4]/td[2]/text()').extract()[0]
			#print(rongdiya_info['native_place'].encode('utf-8'))
		except IndexError:
			rongdiya_info['native_place'] = u""
			print("native_place index eror")

		rongdiya_info['borrow_detail'] = sel.xpath('//div[contains(@class, "pro_vbob3 pane")]/text()').extract()[0]
		#print(rongdiya_info['borrow_detail'].encode('utf-8'))
		rongdiya_info['auto_bid_total_quota'] = sel.xpath('/html/body/div[3]/div[4]/div[1]/div[3]/div[1]/table//tr[3]/td[1]/text()').extract()[0]
		#print(rongdiya_info['auto_bid_total_quota'].encode('utf-8'))
		#for k in rongdiya_info.keys():
		#	print(str(rongdiya_info[k].encode('utf-8')) + str(type(rongdiya_info[k])))
		yield rongdiya_info
		
