

while [ 1 -lt 2 ]; do
	has_crawled_count1=$(wc -l url_has_crawled.rongjinsuo | awk '{print $1}')
	sleep 10m
	has_crawled_count2=$(wc -l url_has_crawled.rongjinsuo | awk '{print $1}')
	if [ $has_crawled_count1 -eq $has_crawled_count2 ]; then
		old_crawl_pid=$(ps aux | grep "rongjinsuo" | grep -v "grep" | awk '{print $2}')
		echo "old_crawl_pid:"$old_crawl_pid
		kill -n 9 $old_crawl_pid
		sh restart.sh
		sleep 10m
		sh auto_restart.sh 
		break
	fi
	echo "crawl is regular"
	cur_time=$(date +'%Y-%m-%d: %H:%M:%S')
	echo $cur_time
done
