import threading 
import cfscrape
import re as regex
import HtmlParsing

class SearchThread(threading.Thread):
	def __init__(self, threadID, scraper, html):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.scraper = scraper
		self.html = html
		self.episodeCount = 0

	def run(self):
		self.episodeCount = getEpisodeCount(self.html, self.scraper)
		
def getAnimeHtml(html, scraper):
	url = 'http://kissanime.to'
	try:
		reg = regex.search(r'"aAnime"\shref="(?P<Link>/Anime/[^"]+)\"\>(?P<AnimeName>[^<]+)', html)
		url += reg.group('Link')
		animeName = reg.group('AnimeName')
	except:
		return '', '', ''

	html = HtmlParsing.getHtml(url, scraper)
	return html, url, animeName

def getEpisodeCount(html, scraper):
	html, url, animeName = getAnimeHtml(html, scraper)
	try:
		html = regex.split(r'\<table\sclass\=\"listing\"\>', html)
		html = regex.split(r'\<\/table\>', html[1])[0]
		regexQuery = '<a\s+?href.*?()'
		reg = regex.findall(regexQuery, html)
		episodeCount = len(reg)
	except:
		print('failed regex @', url)
		log = open('log', 'a')
		log.write('failed regex @' + url + ':\n')
		for i in html:
			log.write(i)
		log.write('\n\n\n\n\n\n\n')	
		log.close()
		episodeCount = -1

	return episodeCount

