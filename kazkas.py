from Utils import *
import re as regex
import sys

url = 'http://ktug.lt/'

def FindRefs(url, depth=0):
	if depth > 3:
		return
	html = GetRequest(url)
	urls = regex.findall(r'href="(?P<html>[^")]+)', html)

	chionsas = regex.findall(r'[C|c]hions', html)
	if len(chionsas) != 0:
		print('---Chionsas ', url)
		sys.exit()
	
	for url in urls:
		if len(regex.findall(r'ktug', url)) != 0:
			print(url)
			FindRefs(url, depth+1)

FindRefs(url)