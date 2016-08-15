# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from weidai.items import *
from hashlib import md5
import MySQLdb
import MySQLdb.cursors
from datetime import datetime
from twisted.enterprise import adbapi
from scrapy import signals

class WeidaiPipeline(object):
	def __init__(self):
		self.homepage_file = open("hompage.json", "wb")
		self.zhibiao_file = open("zhibiao.json", "wb")

	def process_item(self, item, spider):
		if isinstance(item, WeidaiHomeItem):
			line = json.dumps(dict(item)) + "\n"
			self.homepage_file.write(line)
		if isinstance(item, BiaoDiItem):
			line = json.dumps(dict(item)) + "\n"
			self.zhibiao_file.write(line)
		return item


class MySQLStoreWeidaiPipeline(object):
	def __init__(self, conn):
		self.conn = conn
		self.cur = self.conn.cursor()
		count=self.cur.execute('select * from homepage_info')
		print("count = ")
		print(count)
	
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
		now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		if isinstance(item, WeidaiHomeItem):
			self.cur.execute(""" select 1 from homepage_info where url = %s """, (item['url'], ))
			ret = self.cur.fetchone()
			if not ret:
				self.cur.execute(""" INSERT INTO homepage_info (url, total_volume, member, revenue_user, last_updated) \
							VALUES(%s, %s, %s, %s, %s) """, \
							(item['url'], item['total_volume'], item['member'], item['revenue_user'], now))
			else:
				self.cur.execute(""" UPDATE homepage_info SET total_volume = %s, member = %s, revenue_user = %s, last_updated = %s WHERE url = %s""", \
							(item['total_volume'], item['member'], item['revenue_user'], now, item['url']))

		if isinstance(item, BiaoDiItem):
			linkmd5id =str(self._get_linkmd5id(item))
			self.cur.execute("""select 1 from zhibiao_info where linkmd5id = %s """, (linkmd5id, ))
			ret = self.cur.fetchone()
			if not ret:
				print("md5: " + str(linkmd5id))
				self.cur.execute(""" INSERT INTO zhibiao_info (linkmd5id, amount_of_subject, rate_of_return, deadline) \
										VALUES(%s, %s, %s, %s) """, \
										(linkmd5id, item['amount_of_subject'], item['rate_of_return'], item['deadline'])) 

				self.cur.execute(""" UPDATE zhibiao_info SET user_sex = %s, marriage = %s, repayment_periods = %s, repayment_ways = %s WHERE linkmd5id = %s""", \
							(item['user_sex'], item['marriage'], item['repayment_periods'], item['repayment_ways'], linkmd5id)) 

				self.cur.execute(""" UPDATE zhibiao_info SET loan_number = %s, product_type = %s, vehicle_brand = %s, license_plate_number = %s WHERE linkmd5id = %s""", \
							(item['loan_number'], item['product_type'], item['vehicle_brand'], item['license_plate_number'], linkmd5id))

				self.cur.execute(""" UPDATE zhibiao_info SET revenue_passenger_kilometers=%s, purchasing_price=%s,collateral_value=%s,approval_money=%s WHERE linkmd5id=%s""", \
							(item['revenue_passenger_kilometers'], item['purchasing_price'], item['collateral_value'], item['approval_money'], linkmd5id))

				self.cur.execute(""" UPDATE zhibiao_info SET information = %s, today_invest = %s, today_invest_number = %s, today_invest_users = %s WHERE linkmd5id=%s""", \
							(item['information'], item['today_invest'], item['today_invest_number'], item['today_invest_users'], linkmd5id))

				self.cur.execute(""" UPDATE zhibiao_info SET is_hot_invest = %s, new_invest = %s, url = %s, last_updated = %s, title = %s WHERE linkmd5id=%s""", \
							(item['is_hot_invest'], item['new_invest'], item['url'], now, item['title'], linkmd5id))

				self.cur.execute(""" UPDATE zhibiao_info SET  release_date = %s, progress_width = %s, source_of_stores = %s, native_place = %s WHERE linkmd5id=%s""", \
							(item['release_date'], item['progress_width'], item['source_of_stores'], item['native_place'], linkmd5id))

				self.cur.execute(""" UPDATE zhibiao_info SET stay_still = %s, number_of_overdue = %s, verifytime = %s, audit_instructions = %s WHERE linkmd5id=%s""", \
							(item['stay_still'], item['number_of_overdue'], item['verifytime'], item['audit_instructions'], linkmd5id))
				
			
			else:	
				self.cur.execute(""" UPDATE zhibiao_info SET linkmd5id = %s, amount_of_subject = %s, rate_of_return = %s, deadline = %s WHERE linkmd5id = %s""", \
										(linkmd5id, item['amount_of_subject'], item['rate_of_return'], item['deadline'], linkmd5id)) 

				self.cur.execute(""" UPDATE zhibiao_info SET user_sex = %s, marriage = %s, repayment_periods = %s, repayment_ways = %s WHERE linkmd5id = %s""", \
							(item['user_sex'], item['marriage'], item['repayment_periods'], item['repayment_ways'], linkmd5id)) 

				self.cur.execute(""" UPDATE zhibiao_info SET loan_number = %s, product_type = %s, vehicle_brand = %s, license_plate_number = %s WHERE linkmd5id = %s""", \
							(item['loan_number'], item['product_type'], item['vehicle_brand'], item['license_plate_number'], linkmd5id))

				self.cur.execute(""" UPDATE zhibiao_info SET revenue_passenger_kilometers=%s, purchasing_price=%s,collateral_value=%s,approval_money=%s WHERE linkmd5id=%s""", \
							(item['revenue_passenger_kilometers'], item['purchasing_price'], item['collateral_value'], item['approval_money'], linkmd5id))

				self.cur.execute(""" UPDATE zhibiao_info SET information = %s, today_invest = %s, today_invest_number = %s, today_invest_users = %s WHERE linkmd5id=%s""", \
							(item['information'], item['today_invest'], item['today_invest_number'], item['today_invest_users'], linkmd5id))

				self.cur.execute(""" UPDATE zhibiao_info SET is_hot_invest = %s, new_invest = %s, url = %s, last_updated = %s, title = %s WHERE linkmd5id=%s""", \
							(item['is_hot_invest'], item['new_invest'], item['url'], now, item['title'], linkmd5id))

				self.cur.execute(""" UPDATE zhibiao_info SET  release_date = %s, progress_width = %s, source_of_stores = %s, native_place = %s WHERE linkmd5id=%s""", \
							(item['release_date'], item['progress_width'], item['source_of_stores'], item['native_place'], linkmd5id))

				self.cur.execute(""" UPDATE zhibiao_info SET stay_still = %s, number_of_overdue = %s, verifytime = %s, audit_instructions = %s WHERE linkmd5id=%s""", \
							(item['stay_still'], item['number_of_overdue'], item['verifytime'], item['audit_instructions'], linkmd5id))
				
	def _get_linkmd5id(self, item):
		return md5(item['url']).hexdigest()
