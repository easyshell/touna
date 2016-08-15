# coding: utf-8

import csv
import codecs
import MySQLdb as mdb

csvfile = codecs.open('weidaiweb_data.csv', 'wb')
csvfile.write(codecs.BOM_UTF8)
writer = csv.writer(csvfile)

writer.writerow(["标题", "借贷编号", "项目总额", "年化收益", "项目期限", "还款方式", 
					"发布日期", "交易进度", "来源门店", "性别", "婚姻状况", "籍贯", 
					"还清期数", "待还款", "逾期次数", "车辆品牌", "车牌号", "公里数", 
					"购买价格", "抵押估价", "审核时间", "审核说明"])
try:
	conn = mdb.connect(host="10.0.4.123", user="root", passwd="root123", db="weidaiweb_db", port=3306)
	cur = conn.cursor()
	count = cur.execute("select title, loan_number, amount_of_subject, rate_of_return, \
							deadline, repayment_ways, release_date, progress_width,  source_of_stores, \
							user_sex, marriage, native_place, repayment_periods, stay_still, \
							number_of_overdue, vehicle_brand, license_plate_number, revenue_passenger_kilometers, \
							purchasing_price, collateral_value, verifytime, audit_instructions from zhibiao_info")
	print "count=%d" % count
	result = cur.fetchmany(10)
	#print(result)
	writer.writerows(result)
	
except mdb.Error,e:
	print "Mysql Error %d: %s" % (e.args[0], e.args[1])


