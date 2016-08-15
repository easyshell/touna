#-*-coding:utf-8-*-

hostname=10.0.4.123
PORT="3306"
username=root
password=root123

#hostname=localhost
#username=bi
#password=bi123
mysql -h${hostname}  -u${username} -p${password} < create_table.sql

