
CREATE DATABASE IF NOT EXISTS rongjinsuo_db DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE rongjinsuo_db;

CREATE TABLE  IF NOT EXISTS toubiao_info (
	linkmd5id char(200) NOT NULL COMMENT 'url md5',
  	title text COMMENT '标题', 
  	expected_annual_income text COMMENT '预期年化收益',
	lock_time text COMMENT '锁定期',
	project_amount text COMMENT '项目金额', 
	project_number text COMMENT '项目编号',
	repay_method text COMMENT '还款方式',
	use_of_funds text COMMENT '资金用途',
	product_provide text COMMENT '产品提供',
	date_of_invitation text COMMENT '发标日期',
	completion text COMMENT '完成率',
	car_models text COMMENT '车型',
	evaluating_price text COMMENT '评估价',
	record_date text COMMENT '登记日期',
	xinghao text COMMENT '型号',
	appraiser text COMMENT '评估师', 
	borrower text COMMENT '借款人',
	credit_rating text COMMENT '信用等级',
	gender text COMMENT '性别',
	mariage text COMMENT '婚否', 
	education text COMMENT '学历', 
	borrowing_type text COMMENT '借款类型',
	id_number text COMMENT '身份证号',
	age text COMMENT '年龄',
	working_year text COMMENT '在职年限',
	present_address text COMMENT '现居地',
	native_place text COMMENT '户籍地', 
	borrow_detail text COMMENT '借款详情',
	auto_bid_total_quota text COMMENT '自动投标限额', 
	product_classify text COMMENT '产品类型',
	url text COMMENT 'url',
  	last_updated datetime DEFAULT NULL  COMMENT '最后更新时间',
  	PRIMARY KEY (linkmd5id)
) ENGINE=MyISAM DEFAULT CHARSET='utf8';


