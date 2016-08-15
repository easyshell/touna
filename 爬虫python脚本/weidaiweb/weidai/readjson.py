import json
#-*-coding:utf-8-*-

f = file("zhibiao.json")
s = json.load(f)
print(s.keys())
for k in s.keys():
	if not type(s[k]) == int:
		print(str(s[k].encode('utf-8'))+":")
