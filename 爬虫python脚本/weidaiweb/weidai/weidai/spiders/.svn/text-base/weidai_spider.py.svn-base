#!/usr/bin/python
#-*-coding:utf-8-*-
import scrapy
from scrapy import Request
from weidai.items import *
from scrapy.selector import Selector
from scrapy.conf import settings
import requests
import urlparse
from bs4 import BeautifulSoup
import re
import ConfigParser
import sys
import time

class WeidaiSpider(scrapy.Spider):
	name = 'weidaiweb'
	#allowed_domains = ["weidai.com"]
	start_urls = []
	handle_httpstatus_list = [301, 302]

	def __init__(self):
		#self.first_page = 1
		#self.last_page = 1
		self.load_conf()
		self.homepage_url = "https://www.weidai.com.cn/"
		self.zhibiao_base_url = "https://www.weidai.com.cn/bidlist/tenderList?page="
		print(self.homepage_url)
	
	def load_conf(self):
		conf = ConfigParser.ConfigParser()
		conf.read('/home/lznwt/weidaiweb/weidai/weidai/spiders/con.ini')
		print("conf:")
		print(conf.sections())
		first_page = int(conf.get("range", "first_page"))
		last_page = int(conf.get("range", "last_page"))
		self.set_page_range(first_page, last_page)

	def start_requests(self):
		for page_num in range(self.first_page, 1+self.last_page):
			print(page_num)
			cur_url = self.zhibiao_base_url + str(page_num)
			print(cur_url)
			#tr = requests.get(cur_url)
			yield scrapy.http.Request(url=cur_url, callback=self.parse_zhibiao_page)
		print(self.homepage_url)
		yield Request(self.homepage_url, callback=self.parse_homepage)

	def parse_homepage(self, response):
		sel = Selector(text=response.body_as_unicode())
		print(response.url)
		homepage_info = WeidaiHomeItem()
		homepage_info['url'] = response.url
		homepage_info['status_code'] = response.status
		homepage_info['total_volume'] = sel.xpath('/html/body/div[3]/div/div[1]/div/h3/span/text()').extract()[0]
		homepage_info['member'] = sel.xpath('/html/body/div[7]/div[2]/div/p[2]/span[2]/text()').extract()[0]
		homepage_info['revenue_user'] = sel.xpath('/html/body/div[7]/div[2]/div/p[1]/span[2]/text()').extract()[0]
		yield homepage_info
	
	def set_page_range(self, first_page, last_page):
		self.first_page = first_page
		self.last_page = last_page

	def parse_zhibiao_page(self, response):
		sel = Selector(text=response.body_as_unicode())
		print("parse_zhibaio_page")
		hrefs = sel.xpath('/html/body/div[4]/div[2]/dl/dt/a/@href').extract()
		for href in hrefs:
			zhibiao_url = urlparse.urljoin(self.homepage_url, href)
			#zhibiao_url = "https://www.weidai.com.cn/newbid/e1dcbea6c4a21fc14fe19962d2e9d0ea.html"
			yield Request(url=zhibiao_url, callback=self.parse_zhibiao)

	def parse_zhibiao(self, response):
		zhibiao_info = BiaoDiItem()
		for info in zhibiao_info:
			zhibiao_info[info] = ''
		zhibiao_info['repayment_periods'] = 0
		print("parse_zhibiao")
		print(response.url)
		sel = Selector(text=response.body_as_unicode())
		infoul = sel.xpath('//ul[contains(@class, "infoUl")]/li').extract()
		dateul = sel.xpath('//ul[contains(@class, "dateUl")]/li').extract()
		rateul = sel.xpath('//ul[contains(@class, "rateUl")]/li').extract()
		infoul.extend(dateul)
		infoul.extend(rateul)

		for it in infoul:
			#print(type(it.encode('utf-8')))
			itu = it.encode('utf-8')
			#print(itu)
			its = Selector(text=it)
			
			if re.compile(r"性别").search(itu):
				#print(itu)
				zhibiao_info['user_sex'] = its.xpath('//li/text()').extract()[0]
				#print(zhibiao_info['user_sex'])
			if re.compile(r"婚姻状况").search(itu):
				#print(itu)
				zhibiao_info['marriage'] = its.xpath('//li/text()').extract()[0]	
				#print(zhibiao_info['marriage'])
			if re.compile(r"车牌号").search(itu):
				#print(itu)
				zhibiao_info['license_plate_number'] = its.xpath('//span[contains(@id, "chehao")]/text()').extract()[0]
				#print(zhibiao_info['license_plate_number'])
			if re.compile(r"公里数").search(itu):
				#print(itu)
				zhibiao_info['revenue_passenger_kilometers'] = its.xpath('//li/text()').extract()[0]
				#print(zhibiao_info['revenue_passenger_kilometers'])
			
			if re.compile(r"购买价格").search(itu):
				#print(itu)
				zhibiao_info['purchasing_price'] = its.xpath('//li/text()').extract()[0]
				#print(zhibiao_info['purchasing_price'])	
			if re.compile(r"抵押估价").search(itu):
				#print(itu)
				zhibiao_info['collateral_value'] = its.xpath('//li/text()').extract()[0]
				#print(zhibiao_info['collateral_value'])
			if re.compile(r"车辆品牌").search(itu):
				#print(itu)
				zhibiao_info['vehicle_brand'] = its.xpath('//li/text()').extract()[0]
			if re.compile(r"项目期限").search(itu):
				#print(itu)
				zhibiao_info['deadline'] = str(its.xpath('//li[@class="date"]/p/em/text()').extract()[0])
				zhibiao_info['deadline'] += str(its.xpath('//li[@class="date"]/p/text()').extract()[0].encode('utf-8'))
				#print(zhibiao_info['deadline'])
			if re.compile(r"还清期数").search(itu):
				#print(itu)
				zhibiao_info['repayment_periods'] = its.xpath('//li/text()').extract()[0]
				#print(zhibiao_info['repayment_periods'].encode('utf-8'))
			if re.compile(r"还款方式").search(itu):
				#print(itu)
				zhibiao_info['repayment_ways'] = its.xpath('//li/text()').extract()[0]
				#print(zhibiao_info['repayment_ways'])
			if re.compile(r"发布日期").search(itu):
				zhibiao_info['release_date'] = its.xpath('//li/text()').extract()[0]
			
			
			
			if re.compile(r"来源门店").search(itu):
				zhibiao_info['source_of_stores'] = its.xpath('//li/text()').extract()[0]
			if re.compile(r"籍贯").search(itu):
				zhibiao_info['native_place'] = its.xpath('//li/text()').extract()[0]
			if re.compile(r"待还款").search(itu):
				zhibiao_info['stay_still'] = its.xpath('//li/text()').extract()[0]
			if re.compile(r"逾期次数").search(itu):
				zhibiao_info['number_of_overdue'] = its.xpath('//li/text()').extract()[0]
			if re.compile(r"审核时间").search(itu):
				zhibiao_info['verifytime'] = its.xpath('//li/text()').extract()[0]
			if re.compile(r"审核说明").search(itu):
				zhibiao_info['audit_instructions'] = its.xpath('//li/text()').extract()[0]
			if re.compile(r"交易进度").search(itu):
				zhibiao_info['progress_width'] = its.xpath('//li/em/text()').extract()[0]
			if re.compile(r"待还款").search(itu):
				zhibiao_info['stay_still'] = its.xpath('//li/text()').extract()[0]
			
		if 'user_sex' not in zhibiao_info.keys():
			zhibiao_info['user_sex'] = sel.xpath('//div[@id="xinyong"]//td[contains(@class, "item3Content")]/text()').extract()[0]
		if 'marriage' not in zhibiao_info.keys():
			zhibiao_info['marriage'] = sel.xpath('//div[@id="xinyong"]//td[contains(@class, "item2Content")]/text()').extract()[0]
		if 'vehicle_brand' not in zhibiao_info.keys():
			zhibiao_info['vehicle_brand'] = ''
		if 'license_plate_number' not in zhibiao_info.keys():
			zhibiao_info['license_plate_number'] = ''
		if 'revenue_passenger_kilometers' not in zhibiao_info.keys():
			zhibiao_info['revenue_passenger_kilometers'] = ''
		if 'purchasing_price' not in zhibiao_info.keys():
			zhibiao_info['purchasing_price'] = ''
		if 'collateral_value' not in zhibiao_info.keys():
			zhibiao_info['collateral_value'] = ''
		if 'native_place' not in zhibiao_info.keys():
			zhibiao_info['native_place'] = sel.xpath('//div[@id="xinyong"]//td[contains(@class, "item1Content")]/text()').extract()[1]
		if 'stay_still' not in zhibiao_info.keys():
			zhibiao_info['stay_still'] = sel.xpath('//div[@id="xinyong"]//td[contains(@class, "item2Content")]/text()').extract()[2]
		if 'number_of_overdue' not in zhibiao_info.keys():
			zhibiao_info['number_of_overdue'] = sel.xpath('//div[@id="xinyong"]//td[contains(@class, "item3Content")]/text()').extract()[2]
		if 'verifytime' not in zhibiao_info.keys():
			zhibiao_info['verifytime'] = ''
		if 'audit_instructions' not in zhibiao_info.keys():
			zhibiao_info['audit_instructions'] = ''
	
		zhibiao_info['title'] = sel.xpath('//div[contains(@class, "title")]/h1/text()').extract()[0]
		zhibiao_info['progress_width'] = sel.xpath('//div[contains(@class, "progress")]/@data-width').extract()[0]
		zhibiao_info['url'] = response.url
		zhibiao_info['status_code'] = response.status
		zhibiao_info['amount_of_subject'] = sel.xpath('//*[@id="borrowDetialAmount"]/text()').extract()[0]
		zhibiao_info['rate_of_return'] = sel.xpath('//li[@class="profit"]/p/em/text()').extract()[0]
		zhibiao_info['loan_number'] = sel.xpath('//div[@class="number"]/text()').extract()[0]
		zhibiao_info['product_type'] = ''
		zhibiao_info['approval_money'] = ''
		zhibiao_info['information'] = ''
		zhibiao_info['today_invest']= ''
		zhibiao_info['today_invest_number'] = ''
		zhibiao_info['today_invest_users'] = ''
		zhibiao_info['is_hot_invest'] = ''
		zhibiao_info['new_invest' ] =  ''
				
#		"""
#		zhibiao_info['collateral_value'] = ''
#		zhibiao_info['timing_invest'] = ''
#		zhibiao_info['orientation_invest'] = ''
#		zhibiao_info['transfer_invest'] = ''
#		zhibiao_info['credit_invest'] = ''
#		zhibiao_info['optimization_plan'] = ''
#		zhibiao_info['data_capsule'] = ''
#		"""
		yield zhibiao_info
	
