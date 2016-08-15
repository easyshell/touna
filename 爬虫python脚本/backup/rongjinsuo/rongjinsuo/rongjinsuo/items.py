# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item

class RongJinSuoItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	url = Field()
	title = Field()
	expected_annual_income = Field() #预期年化收益
	lock_time = Field() #锁定期
	project_amount = Field() #项目金额
	project_number = Field() #项目编号
	repay_method = Field() #还款方式
	use_of_funds = Field() #资金用途
	product_provide = Field() #产品提供
	date_of_invitation = Field() #发标日期
	completion = Field() #完成率
	car_models = Field() #车型
	evaluating_price = Field() #评估价 
	record_date = Field() #登记日期
	xinghao = Field() #型号
	appraiser = Field() #评估师
	borrower = Field() #借款人
	credit_rating = Field() #信用等级
	gender = Field() #性别
	mariage = Field() #婚否
	education  = Field() #学历
	borrowing_type = Field() #借款类型
	id_number = Field() #身份证号
	age = Field() # 年龄
	working_year = Field() #在职年限	
	present_address = Field() #现居地
	native_place = Field() #户籍地
	borrow_detail = Field() #借款详情
	auto_bid_total_quota = Field() #自动投标总限额
	product_classify = Field() #产品类型

