PATH="/usr/lib64/qt-3.3/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin"
export $PATH
export LD_LIBRARY_PATH=/usr/local/lib

root=$(cd "$(dirname "$0")"; pwd)
gettoubiaourls_home=$root/../gettoubiaourls
cd $gettoubiaourls_home
nohup scrapy crawl gettoubiaourls > gettoubiaourls.log 2>&1 &
while [ 1 -lt 2 ]; do
	sleep 10m
	count=$(ps aux | grep "rongjinsuo" | wc -l)
	if [ $count -eq 1 ]; then
		break
	fi
done

cd $root
rm -f url.all
rm -f url.must
rm -f url_has_crawled.rongjinsuo
rm -f url.crawled
cp -f $gettoubiaourls_home/url_seeds/toubiao_urls.rongjinsuo.$(date +"%Y-%m-%d") ./url.all
sort -u url.all > all.url; cp -f all.url url.all

nohup scrapy crawl rongjinsuo -a seed_file="url.all" > rongjinsuo.log 2>&1 &
sleep 10m
nohup sh auto_restart.sh > auto_restart.log 2>&1 &
