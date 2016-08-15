# coding: utf-8

import csv
import codecs
import MySQLdb as mdb
import ConfigParser

csvfile = codecs.open('rongjinsuo_data.csv', 'wb')
csvfile.write(codecs.BOM_UTF8)
writer = csv.writer(csvfile)

head = []
with open("rongjinsuo.field", "r") as f:
	lines = f.readlines()
	for line in lines:
		field = line.strip()
		head.append(field)

writer.writerow(head)
try:
	conn = mdb.connect(host="10.0.4.123", user="root", passwd="root123", db="rongjinsuo_db", port=3306)
	cur = conn.cursor()
	
	count = cur.execute("select title, expected_annual_income, lock_time, project_amount \
							, project_number, repay_method, use_of_funds, product_provide,  date_of_invitation \
							, completion, car_models, evaluating_price, record_date, xinghao \
						    , appraiser, borrower, credit_rating, gender \
							, mariage, education, borrowing_type, id_number, age, working_year \
							, present_address, native_place, borrow_detail, auto_bid_total_quota,  product_classify from toubiao_info")
	print "count=%d" % count
	result = cur.fetchmany(10)
	#print(result)
	writer.writerows(result)
	
except mdb.Error,e:
	print "Mysql Error %d: %s" % (e.args[0], e.args[1])
