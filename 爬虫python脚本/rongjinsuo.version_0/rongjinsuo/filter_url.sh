
has_crawl=$1
all_url=$2

awk '{
	if (ARGIND==1) {
		block[$1] = 1
	} else if (2==ARGIND) {
		if (block[$1] != 1) {
			print $1
		}
	}
}' $has_crawl $all_url 
