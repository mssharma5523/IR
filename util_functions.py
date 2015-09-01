import re
from re import *

def getTitle(text):
    titleRE = re.compile("<title>(.+?)</title>")
    title = titleRE.search(text).group(1)
    return title


def getRelevantText(content, query):
	words = query.split()
	result = ""
	arr = []
	for word in words:
		l = content.find(word)
		r = l + len(word)
		tem = [l-15, r+15]
		arr.append(tem)
	arr.sort(key=lambda x: x[0])
	b = []
	cur = 0
	for a in arr:
		if(cur == 0):
			b.append(a)
			cur += 1
		else:
			if(b[cur-1][1] > a[0]):
				b[cur-1][1] = max(b[cur-1][1],a[1])
			else:
				b.append(a)
				cur += 1
	for c in b:
		result += content[c[0]:c[1]]
	result = ' '.join(result.split())
	return result

