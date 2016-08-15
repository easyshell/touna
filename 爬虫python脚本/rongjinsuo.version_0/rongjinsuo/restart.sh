sh iterative_crawl.sh
nohup scrapy crawl rongjinsuo -a seed_file="url.next" > log.txt 2>&1 &
