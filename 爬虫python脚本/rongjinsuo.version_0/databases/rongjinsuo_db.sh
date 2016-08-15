#-*-coding:utf-8-*-

hostname=10.0.4.123
PORT="3306"
username=root
password=root123
db_name=rongjinsuo_db
table_zhibiao=toubiao_info

#hostname=localhost
#username=bi
#password=bi123
#db_name=rongjinsuo_db
#table_toubiao=toubiao_info

mysql -h${hostname}  -u${username} -p${password} < create_table.sql

