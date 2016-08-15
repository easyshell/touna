import re

f = open('one.page')
text = f.read()
#print(text)


pat = re.compile("/jQuery110203868564622439057_1470880995693\(([\s\S]*)\);([\s]*)$")
print(pat.search(text).group(1))
