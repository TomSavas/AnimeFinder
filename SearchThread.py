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
		self.episodeCount = ''

	def run(self):
		try:
			self.episodeCount = getEpisodeCount(self.html, self.scraper)
		except:
			print('CFscrape was unable to bypass cloudflare...')

def getAnimeHtml(html, scraper):
	url = 'http://kissanime.to'
	try:
		reg = regex.search(r'"aAnime"\shref="(?P<Link>/Anime/[^"]+)', html)
		url += reg.group('Link')
	except:
		return ''

	html = HtmlParsing.getHtml(url, scraper)
	return html, url

def getEpisodeCount(html, scraper):
	html, url = getAnimeHtml(html, scraper)

	try:
		reg = regex.search(r'Episode\s(?P<EpisodeCount>\d+)', html)
		episodeCount = reg.group('EpisodeCount')
	except:
		print('failed regex @', url)
		log = open('log', 'a')
		log.write('failed regex @' + url + ':\n' + html + '\n\n\n\n\n\n\n')
		log.close()
		episodeCount = 'ERROR'

	return episodeCount

