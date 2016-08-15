
CREATE DATABASE IF NOT EXISTS weidaiweb_db DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE weidaiweb_db;

CREATE TABLE  IF NOT EXISTS zhibiao_info (
  linkmd5id char(200) NOT NULL COMMENT 'url md5',
  amount_of_subject text COMMENT '项目总额',
  rate_of_return text COMMENT '年化收益',
  deadline text  COMMENT '项目期限',
  user_sex text  COMMENT '借款用户性别',
  marriage text  COMMENT '借款用户婚姻',
  repayment_periods text  COMMENT '还清期数',
  repayment_ways text  COMMENT '还款方式',
  loan_number text  COMMENT '借款编号',
  product_type text  COMMENT '产品类型',
  vehicle_brand text  COMMENT '车辆品牌',
  license_plate_number text  COMMENT '车牌号',
  revenue_passenger_kilometers text  COMMENT '公里数',
  purchasing_price text  COMMENT '购买价格',
  collateral_value text  COMMENT '抵押价格',
  approval_money text  COMMENT '核批金额',
  information text  COMMENT '审核资料',
  today_invest text  COMMENT '今日投资额',
  today_invest_number text  COMMENT '今日投资笔数',
  today_invest_users text  COMMENT '今日投资用户数',
  is_hot_invest text  COMMENT '热售标',
  new_invest text  COMMENT '新手标',
  url text  COMMENT 'url',
  title text COMMENT '标题',
  release_date text COMMENT '发布日期',
  progress_width text COMMENT '交易进度',
  source_of_stores text COMMENT '来源门店',
  native_place text COMMENT '籍贯', 
  stay_still text COMMENT '待还款',
  number_of_overdue text COMMENT '逾期次数',
  verifytime text COMMENT '审核时间',
  audit_instructions text COMMENT '审核说明',
  last_updated datetime DEFAULT NULL  COMMENT '最后更新时间',
  PRIMARY KEY (linkmd5id)
) ENGINE=MyISAM DEFAULT CHARSET='utf8';


CREATE TABLE IF NOT EXISTS homepage_info (
  url char(200)  COMMENT 'url',
  total_volume text  COMMENT '累计成交额',
  member text COMMENT '会员人数',
  revenue_user text COMMENT '用户收益',
  last_updated datetime DEFAULT NULL  COMMENT '最后更新时间',
  PRIMARY KEY (url)
) ENGINE=MyISAM DEFAULT CHARSET='utf8';


