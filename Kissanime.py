from HtmlParsing import *

try:
	animeInfo = getAnimeInfo()
	for i in animeInfo:
		print(i)
except:
	print('CFscrape was unable to bypass cloudflare...')
