# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from rongjinsuo.items import *
from hashlib import md5
import MySQLdb
import MySQLdb.cursors
from datetime import datetime
from twisted.enterprise import adbapi
from scrapy import signals

class RongJinSuoPipeline(object):
	def __init__(self):
		self.toubiao_file = open("toubiao.json", "wb")

	def process_item(self, item, spider):
		if isinstance(item, RongJinSuoItem):
			line = json.dumps(dict(item)) + "\n"
			self.toubiao_file.write(line)
		return item

class MySQLStoreRongJinSuoPipeline(object):
	def __init__(self, conn):
		self.conn = conn
		self.cur = self.conn.cursor()
	
	@classmethod	
	def from_settings(cls, settings):
		print("read settings from setting.py")
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
		now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		if isinstance(item, RongJinSuoItem):
			linkmd5id =str(self._get_linkmd5id(item))
			self.cur.execute("""select 1 from toubiao_info where linkmd5id = %s """, (linkmd5id, ))
			ret = self.cur.fetchone()
			if not ret:
				print("md5: " + str(linkmd5id))
				self.cur.execute(""" INSERT INTO toubiao_info (linkmd5id, title, expected_annual_income, lock_time) \
										VALUES(%s, %s, %s, %s) """, \
										(linkmd5id, item['title'], item['expected_annual_income'], item['lock_time'])) 

				self.cur.execute(""" UPDATE toubiao_info SET project_amount = %s, project_number = %s, repay_method = %s, use_of_funds = %s WHERE linkmd5id = %s""", \
							(item['project_amount'], item['project_number'], item['repay_method'], item['use_of_funds'], linkmd5id)) 
				

				self.cur.execute(""" UPDATE toubiao_info SET product_provide = %s, date_of_invitation = %s, completion = %s, car_models = %s WHERE linkmd5id = %s""", \
							(item['product_provide'], item['date_of_invitation'], item['completion'], item['car_models'], linkmd5id))
				
				self.cur.execute(""" UPDATE toubiao_info SET evaluating_price=%s, record_date=%s,xinghao=%s,appraiser=%s WHERE linkmd5id=%s""", \
							(item['evaluating_price'], item['record_date'], item['xinghao'], item['appraiser'], linkmd5id))

				self.cur.execute(""" UPDATE toubiao_info SET borrower = %s, credit_rating = %s, gender = %s, mariage = %s WHERE linkmd5id=%s""", \
							(item['borrower'], item['credit_rating'], item['gender'], item['mariage'], linkmd5id))

				self.cur.execute(""" UPDATE toubiao_info SET education = %s, borrowing_type = %s, id_number = %s, age = %s WHERE linkmd5id=%s""", \
							(item['education'], item['borrowing_type'], item['id_number'], item['age'], linkmd5id))

				self.cur.execute(""" UPDATE toubiao_info SET  working_year = %s, present_address = %s, native_place = %s, borrow_detail = %s WHERE linkmd5id=%s""", \
							(item['working_year'], item['present_address'], item['native_place'], item['borrow_detail'], linkmd5id))

				self.cur.execute(""" UPDATE toubiao_info SET auto_bid_total_quota = %s, product_classify = %s, url=%s, last_updated = %s WHERE linkmd5id=%s""", \
							(item['auto_bid_total_quota'], item['product_classify'], item['url'], now, linkmd5id))

			else:	
				
				self.cur.execute(""" UPDATE toubiao_info set title=%s, expected_annual_income=%s, lock_time=%s WHERE linkmd5id = %s""", \
							(item['title'], item['expected_annual_income'], item['lock_time'], linkmd5id))

				self.cur.execute(""" UPDATE toubiao_info SET project_amount = %s, project_number = %s, repay_method = %s, use_of_funds = %s WHERE linkmd5id = %s""", \
							(item['project_amount'], item['project_number'], item['repay_method'], item['use_of_funds'], linkmd5id)) 
				

				self.cur.execute(""" UPDATE toubiao_info SET product_provide = %s, date_of_invitation = %s, completion = %s, car_models = %s WHERE linkmd5id = %s""", \
							(item['product_provide'], item['date_of_invitation'], item['completion'], item['car_models'], linkmd5id))
				
				self.cur.execute(""" UPDATE toubiao_info SET evaluating_price=%s, record_date=%s,xinghao=%s,appraiser=%s WHERE linkmd5id=%s""", \
							(item['evaluating_price'], item['record_date'], item['xinghao'], item['appraiser'], linkmd5id))

				self.cur.execute(""" UPDATE toubiao_info SET borrower = %s, credit_rating = %s, gender = %s, mariage = %s WHERE linkmd5id=%s""", \
							(item['borrower'], item['credit_rating'], item['gender'], item['mariage'], linkmd5id))

				self.cur.execute(""" UPDATE toubiao_info SET education = %s, borrowing_type = %s, id_number = %s, age = %s WHERE linkmd5id=%s""", \
							(item['education'], item['borrowing_type'], item['id_number'],  item['age'], linkmd5id))

				self.cur.execute(""" UPDATE toubiao_info SET  working_year = %s, present_address = %s, native_place = %s, borrow_detail = %s WHERE linkmd5id=%s""", \
							(item['working_year'], item['present_address'], item['native_place'], item['borrow_detail'], linkmd5id))

				self.cur.execute(""" UPDATE toubiao_info SET auto_bid_total_quota = %s, product_classify = %s, url=%s, last_updated = %s WHERE linkmd5id=%s""", \
							(item['auto_bid_total_quota'], item['product_classify'], item['url'], now, linkmd5id))

	def _get_linkmd5id(self, item):
		return md5(item['url']).hexdigest()
