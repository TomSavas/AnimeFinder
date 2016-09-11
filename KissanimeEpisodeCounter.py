from HtmlParsing import *

try:
	animeInfo = getAnimeInfo()
	for i in animeInfo:
		print(i)
except:
	print('Something went wrong... (Best error msg ever, I know <3)')



