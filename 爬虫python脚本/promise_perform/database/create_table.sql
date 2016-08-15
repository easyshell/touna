
CREATE DATABASE IF NOT EXISTS promise_perform_db DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE promise_perform_db;

CREATE TABLE  IF NOT EXISTS execut_info (
  info_md5 CHAR(200) NOT NULL COMMENT 'info md5',
  court_name text COMMENT '执行法院',
  area_name  text COMMENT '省份', 
  case_code    text COMMENT '案号',
  duty       text COMMENT '生效法律文书确定的义务',
  performance text COMMENT '被执行人履行情况', 
  disrupt_type_name text COMMENT '失信被执行人行为具体情形',
  publish_date text COMMENT '发布日期',
  iname text COMMENT '姓名',
  card_num text COMMENT '身份证号', 
  sexy text COMMENT '性别',
  age text COMMENT '年龄', 
  last_updated datetime DEFAULT NULL  COMMENT '最后更新时间',
  PRIMARY KEY (info_md5)
) ENGINE=MyISAM DEFAULT CHARSET='utf8';
