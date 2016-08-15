# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#-*-coding:utf-8-*-
import json
from shixin.items import *
import MySQLdb
import MySQLdb.cursors
from datetime import datetime
import re
from hashlib import md5

class ShixinPipeline(object):
	def __init__(self, conn):
		self.file = open('items.j1', 'wb')
		self.conn = conn
		self.cur = self.conn.cursor()
		self.fields = ['iname', 'cardNum', 'caseCode', 'age', 'sexy', 'areaName', 'courtName', 'duty', 'performance', 'disruptTypeName', 'publishDate']

	@classmethod	
	def from_settings(cls, settings):
		dbargs = dict(
			host = settings['MYSQL_HOST'],
			db = settings['MYSQL_DBNAME'],
			user = settings['MYSQL_USER'],
			passwd = settings['MYSQL_PASSWD'],
			charset = 'utf8',
			use_unicode = True
		)
		try:
			conn = MySQLdb.connect(host=dbargs['host'], db=dbargs['db'], user=dbargs['user'], passwd=dbargs['passwd'], charset='utf8')
		except MySQLdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])
		return cls(conn)
		
	def process_item(self, item, spider):
		print("pipeline:\n")
		if isinstance(item, ShixinItem):
			#print(type(item['body']))
			pat = re.compile("/jQuery110203868564622439057_1470880995693\(([\s\S]*)\);([\s]*)$")
			item['body'] = eval(pat.search(item['body']).group(1))
			shixinjson = item['body']
			shixin_executs = shixinjson['data'][0]['result']
			#print(type(shixin_executs))
			#print(len(shixin_executs))
			
			for execut_info in shixin_executs:
				for key in self.fields:
					if not execut_info.has_key(key):
						execut_info[key] = ""
					if type(execut_info[key]) == int:
						execut_info[key] = str(execut_info[key])
				info = str(execut_info['iname'])+str(execut_info['cardNum'])+str(execut_info['caseCode'])+str(execut_info['courtName'])+str(execut_info['duty']) \
						+str(execut_info['areaName'])+str(execut_info['sexy'])+str(execut_info['age'])+str(execut_info['disruptTypeName'])+str(execut_info['performance']) \
						+str(execut_info['publishDate'])
				info_md5 = str(md5(info).hexdigest())
				now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")	
				self.cur.execute(""" SELECT 1 FROM execut_info WHERE info_md5 = %s """, (info_md5,))
				ret = self.cur.fetchone()
				if ret:
					continue	
				try: 
					self.cur.execute(""" INSERT INTO execut_info (info_md5, court_name, area_name, case_code, duty, \
							 performance, disrupt_type_name, publish_date, \
							  iname, card_num, sexy, age, last_updated) \
							 VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, \
							 (info_md5, execut_info['courtName'], execut_info['areaName'], execut_info['caseCode'], \
							  execut_info['duty'], execut_info['performance'], execut_info['disruptTypeName'], \
							  execut_info['publishDate'], execut_info['iname'], execut_info['cardNum'], \
							  execut_info['sexy'], execut_info['age'], now))
				except:
					self.file.write(str(item['url'])+"\n"+str(info_md5)+"\n")
		return item
