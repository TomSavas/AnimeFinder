from KissCrawler import *
from Debug import *

kissCrawler = KissCrawler() 
if len(sys.argv) == 1:
	Debug.debugEnabled = False
elif sys.argv[2].split[0] == "log":
	if sys.argv[2].split[1] == "T":
		Debug.debugEnabled = True
	if sys.argv[2].split[1] == "F":
		Debug.debugEnabled = False
else:
	print("Usage: python3 LaunchCrawler.py log=[T/F]")
	return
kissCrawler.CrawlForAnime()