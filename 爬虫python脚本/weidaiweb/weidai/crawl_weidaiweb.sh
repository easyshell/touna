

PATH="/usr/lib64/qt-3.3/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin"
export $PATH
export LD_LIBRARY_PATH=/usr/local/lib
project_home="/home/lznwt/svn/爬虫python脚本/weidaiweb/weidai"
cd $project_home;
pwd>>a.out;
echo $PATH >> a.out
nohup scrapy crawl weidaiweb >> log.txt 2>&1 &

