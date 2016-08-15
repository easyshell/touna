sort -u url_has_crawled.rongjinsuo > url.crawled
sh filter_url.sh url.crawled url.all > url.must
cp -f url.must url.next

