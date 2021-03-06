#!/usr/bin/python
#-*-coding:utf-8-*-
import re
import sys
import json
import time
import copy
import scrapy
import logging
import requests
import urlparse
import ConfigParser
from scrapy import Request
from datetime import datetime
from bs4 import BeautifulSoup
from main.main_1 import code
from scrapy.conf import settings
from scrapy.selector import Selector
from collections import defaultdict
from scrapy.http import HtmlResponse
from bottle import run, post, request

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='shixin_court_interface_server.logging',
                filemode='w')

class ShixinCourtSpider(scrapy.Spider):
	start_urls = []

	def __init__(self):
		self.useful = [ "iname", "caseCode", "age", "sexy", "cardNum", \
						"courtName", "areaName", "partyTypeName", "gistId", \
						"regDate", "gistUnit", "duty", "performance", \
						"disruptTypeName", "publishDate"
					  ]

	def get_format_date_time(self):
		UTC_FORMAT = "%a %b %d %Y %H:%M:%S"
		sufix = " GMT 0800 (中国标准时间)"
		now = datetime.strftime(datetime.utcnow(), UTC_FORMAT) + sufix
		return now

	def get_index_cookies(self):
		url = "http://shixin.court.gov.cn/"
		headers = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Accept-Language':'zh-CN,zh;q=0.8',
			'Cache-Control':'max-age=0',
			'Connection':'keep-alive',
			'Host':'shixin.court.gov.cn',
			'Upgrade-Insecure-Requests':'1',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.70 Safari/537.36'
		}
		r = requests.get(url, headers=headers)
		#print(r.content)
		yunsuo_session_verify = "yunsuo_session_verify=" + r.cookies['yunsuo_session_verify'] + ";" if 'yunsuo_session_verify' in r.cookies else ""
		route = "route=" + r.cookies['route'] + ";" if 'route' in r.cookies else ""
		JSESSIONID = "JSESSIONID=" + r.cookies['JSESSIONID'] + ";" if 'JSESSIONID' in r.cookies else ""
		cookie_str = yunsuo_session_verify + route + JSESSIONID
		return cookie_str

	def get_image_jsp_cookies(self, cookies_index):
		headers = {
			'Accept':'image/webp,image/*,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Accept-Language':'zh-CN,zh;q=0.8',
			'Connection':'keep-alive',
			'Host':'shixin.court.gov.cn',
			'Referer':'http://shixin.court.gov.cn/',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.70 Safari/537.36'
		}
		headers["Cookie"] = cookies_index
		url = "http://shixin.court.gov.cn/image.jsp"
		r = requests.get(url, headers=headers)
		JSESSIONID = "JSESSIONID=" + r.cookies['JSESSIONID'] + ";" if 'JSESSIONID' in r.cookies else ""
		cookie_str = cookies_index + JSESSIONID
		return cookie_str

	def get_cookies_and_verifycode(self, img_jsp_cookies):
		headers = {
			'Accept':'image/webp,image/*,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Accept-Language':'zh-CN,zh;q=0.8',
			'Connection':'keep-alive',
			'Host':'shixin.court.gov.cn',
			'Referer':'http://shixin.court.gov.cn/',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.70 Safari/537.36'
		}
		url = "http://shixin.court.gov.cn/image.jsp?date="
		date_format = self.get_format_date_time()
		url += date_format
		headers["Cookie"] = img_jsp_cookies
		r = requests.get(url, headers=headers)
		req_cookie_array = img_jsp_cookies.split(";")
		yunsuo_session_verify = ""
		route = ""
		JSESSIONID = ""
		for ck in req_cookie_array:
			if ck.find("yunsuo_session_verify") != -1:
				yunsuo_session_verify = ck + ";"
			if ck.find("route") != -1:
				route = ck + ";"
			if ck.find("JSESSIONID") != -1:
				JSESSIONID = ck + ";"
		if 'yunsuo_session_verify' in r.cookies:
			yunsuo_session_verify = "yunsuo_session_verify=" + r.cookies['yunsuo_session_verify'] + ";"
		cookie_str = yunsuo_session_verify + route + JSESSIONID
		
		pic = "shixin.jpg"
		with open(pic, "wb") as f:
			f.write(r.content)
		auth_code = code(pic)
		return auth_code, cookie_str

	def get_cookies_and_findd(self, name="", cardnum="", province=0):
		cookies_index = self.get_index_cookies()
		img_jsp_cookies = self.get_image_jsp_cookies(cookies_index)
		auth_code, verify_cookies = self.get_cookies_and_verifycode(img_jsp_cookies)
		print "%s, %s" % (auth_code, verify_cookies)
		
		headers = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate',
			'Accept-Language':'zh-CN,zh;q=0.8',
			'Cache-Control':'max-age=0',
			'Connection':'keep-alive',
			'Content-Length':'66',
			'Content-Type':'application/x-www-form-urlencoded',
			'Host':'shixin.court.gov.cn',
			'Origin':'http://shixin.court.gov.cn',
			'Referer':'http://shixin.court.gov.cn/',
			'Upgrade-Insecure-Requests':'1',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.70 Safari/537.36'
		}
		headers["Cookie"] = verify_cookies
		form_data = {
			'pName':name,
			'pCardNum':'',
			'pProvince':'0',
			'pCode':auth_code
		}
		url = "http://shixin.court.gov.cn/findd"
		r = requests.post(url, data = form_data, headers=headers)
		status_code, execute_info = self.parse_shixin_execute_info(r, verify_cookies)
		return status_code, execute_info

	def parse_shixin_execute_info(self, response, verify_cookies):
		if re.compile(r"验证码错误，请重新输入").search(response.content):
			return 300, []

		sel = Selector(text=response.content)
		ids = sel.xpath('//table/tbody//tr//td/a[contains(@class, "View")]/@id').extract()
		headers = {
			'Accept':'*/*',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Accept-Language':'zh-CN,zh;q=0.8',
			'Connection':'keep-alive',
			'Host':'shixin.court.gov.cn',
			'Referer':'http://shixin.court.gov.cn/',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.70 Safari/537.36',
			'X-Requested-With':'XMLHttpRequest'
		}
		headers["Cookie"] = verify_cookies
		if not ids:
			return 200, []
		status_code, execute_info = self.get_detail_info_from_ids(ids)
		return status_code, execute_info
	
	def get_detail_info_from_ids(self, ids):
		execute_info = []
		for idx in ids:
			print(idx)
			verify_count = 0
			while True:
				try:
					headers = { 
                            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Encoding':'gzip, deflate, sdch',
                            'Accept-Language':'zh-CN,zh;q=0.8',
                            'Cache-Control':'max-age=0',
                            'Connection':'keep-alive',
                            'Host':'shixin.court.gov.cn',
                            'Upgrade-Insecure-Requests':'1',
                            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
                    }   
					r = requests.get("http://shixin.court.gov.cn/image.jsp", headers=headers)
					print(r.status_code)
					verify_pic = "shixin_verify.jpg"
					with open(verify_pic, 'wb') as f:
						f.write(r.content)
					auth_code = code(verify_pic)
					print(auth_code)
					cookie_dict = requests.utils.dict_from_cookiejar(r.cookies)
					yunsuo_session_verify = cookie_dict['yunsuo_session_verify'] if cookie_dict.has_key('yunsuo_session_verify') else ""
					JSESSIONID = cookie_dict['JSESSIONID'] if cookie_dict.has_key("JSESSIONID") else ""
					route = cookie_dict['route'] if cookie_dict.has_key("route") else ""
					set_cookie = r.headers['Set-Cookie'].split(',')
					
					if not JSESSIONID:
						for cookie in set_cookie:
							if coookie.find("JSESSIONID"):
								JSESSIONID = cookie[coookie.find("=")+1:]
					if not route:
						for cookie in set_cookie:
							if cookie.find("route"):
								route = cookie[cookie.find("=")+1:]
				
					image_cookie = "yunsuo_session_verify="+yunsuo_session_verify+";" \
                                        +"JSESSIONID="+JSESSIONID+";" \
                                        +"route="+route
					break
				except Exception, e:
					print(e)
					verify_count += 1
					if verify_count > 10:
						return 300, []
					else:
						time.sleep(0.1)

			detail_url = "http://shixin.court.gov.cn/findDetai?id=" + str(idx) + "&pCode=" + auth_code
			headers = {
				'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				'Accept-Encoding':'gzip, deflate, sdch',
				'Accept-Language':'zh-CN,zh;q=0.8',
				'Cache-Control':'max-age=0',
				'Connection':'keep-alive',
				'Host':'shixin.court.gov.cn',
				'Upgrade-Insecure-Requests':'1',
				'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143',
				'Cookie':image_cookie
			}
			r = requests.get(detail_url, headers=headers)
			r.encoding = 'UTF-8'
			try:
				info_dict = eval(r.text)
			except Exception, e:
				info_dict = json.loads(r.content)
			need_info = {}
			for field in self.useful:
				need_info[field] = info_dict[field] if info_dict.has_key(field) else ""
			execute_info.append(need_info)
		return 200, execute_info

	def get_shixin_execute_info(self, name="", cardnum="", province=0):
		status_code, execute_info = self.get_cookies_and_findd(name, cardnum, province)
		result_dict = {}
		result_dict["status_code"] = str(status_code)
		result_dict["execute_info"] = execute_info
		result = json.dumps(result_dict)
		return result

class ShixinFromSpider(scrapy.Spider):
	def __init__(self):
		self.useful = [ "iname", "caseCode", "age", "sexy", "cardNum", \
						"courtName", "areaName", "partyTypeName", "gistId", \
						"regDate", "gistUnit", "duty", "performance", \
						"disruptTypeName", "publishDate"
					  ]
	
	def get_shixin_execute_info_from(self, name="", cardnum="", province=0):
		url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=%E5%A4%B1%E4%BF%A1%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA%E5%90%8D%E5%8D%95&cardNum=&iname=%E6%9D%A8%E4%B9%A6%E5%BC%BA&areaName=&ie=utf-8&oe=utf-8&format=json&t=1477625563536&cb=jQuery1102024190048105083406_1477625164164&_=1477625164181"
		headers = {
			'Accept':'*/*',
			'Accept-Encoding':'gzip,deflate,sdch',
			'Accept-Language':'zh-CN,zh;q=0.8',
			'Connection':'keep-alive',
			'Host':'sp0.baidu.com',
			'Referer':'https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E5%A4%B1%E4%BF%A1%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA%E5%90%8D%E5%8D%95&oq=%E5%A4%B1%E4%BF%A1%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA%E5%90%8D%E5%8D%95&rsv_pq=e9f003180000850f&rsv_t=216c7P0ZDISrLnGkOcr7tqV8iTJSDzHhvNJl3o5YlLGJSWLK%2FRROXfIyfJA&rqlang=cn&rsv_enter=0&rsv_sug3=12&rsv_sug1=10&rsv_sug7=100&prefixsug=%E5%A4%B1%E4%BF%A1%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA%E5%90%8D%E5%8D%95&rsp=0&rsv_sug4=2823&rsv_sug=1',

			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
		}	 
		query_params = {
			'resource_id':'6899',
			'query':'失信被执行人名单',
			'cardNum':cardnum,
			'iname':name,
			'areaName':'',
			'ie':'utf-8',
			'oe':'utf-8',
			'format':'json',
			't':'1477625563536',
			'cb':'jQuery1102024190048105083406_1477625164164',
			'_':'1477625164181'
		}
		r = requests.get(url, headers = headers, params=query_params)
		status_code, execute_info = self.parse_shixin_execute_info(r)
		return status_code, execute_info
		
	def parse_shixin_execute_info(self, response):
		execute_info = []
		pat = re.compile("/jQuery1102024190048105083406_1477625164164\(([\s\S]*)\);([\s]*)$")
		info = eval(pat.search(response.content).group(1))
		if 0 == len(info['data']):
			return 200, [] #201
		execute_list = info['data'][0]['result']
		for detail in execute_list:
			need_info = {}
			for field in self.useful:
				need_info[field] = detail[field] if detail.has_key(field) else ""
			execute_info.append(need_info)
		if not execute_info:
			return 200, execute_info #201
		return 200, execute_info
	
	def get_shixin_execute_info(self, name="", cardnum="", province=0):
		status_code, execute_info = self.get_shixin_execute_info_from(name, cardnum, province)
		result_dict = {}
		result_dict['status_code'] = str(status_code)
		result_dict['execute_info'] = execute_info
		result = json.dumps(result_dict)
		return result

def transform_standard(name="", cardnum="", province=0):
	result = get_shixin_execute_info_interface(name, cardnum, province)
	result_dict = json.loads(result)
	status_code = result_dict['status_code']
	if status_code == "200":
		result_dict['message'] = ""
		for single_info in result_dict['execute_info']:
			for key in single_info:
				tran_key = key.encode('utf-8')
				tran_value = single_info[key].encode('utf-8')
				del single_info[key]
				single_info[tran_key] = tran_value
	elif status_code == "300":
		result_dict['status_code'] = "500"
		result_dict['message'] = "获取失信执行信息失败"
	
   	result = json.dumps(result_dict)
	return result

def get_shixin_execute_info_interface(name="", cardnum="", province=0):
	shixin_interface  = ShixinFromSpider()
	result = shixin_interface.get_shixin_execute_info(name, cardnum, province)
	result_dict = eval(result)
	status_code = result_dict['status_code'] if result_dict.has_key('status_code') else ""
	if status_code == "200":
		return result
	shixin_interface = ShixinCourtSpider()
	result = shixin_interface.get_shixin_execute_info(name, cardnum, province)
	status_code = result_dict['status_code'] if result_dict.has_key('status_code') else ""
	return result

@post('/execute_info')
def get_shixin_execute_information(province=0):
	try:
		name = request.forms.get("name")
		cardnum = request.forms.get("cardnum")
		print "name = %s, cardnum = %s" % (name, cardnum)
		logging.debug("name = " + str(name) + "; " +  "cardnum = " + str(cardnum))
		result = transform_standard(name, cardnum)
	except Exception as e:
		print(e)
		return []
	return result

run(host="0.0.0.0", port=8080)

