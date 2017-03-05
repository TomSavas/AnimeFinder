from Utils import *
from KissParser import *

class KissCrawler(threading.Thread):
	def __init__(self, html=None, crawledPageNumber=None):
		threading.Thread.__init__(self)
		self.scraper = GetScraper()
		self.animeEntities = []
		self.crawlers = []
		self.kissParsers = []
		self.html = html
		self.episodePageLinks = {}
		self.crawledPageNumber = crawledPageNumber

	def run(self):
		self.GatherAnime(self.crawledPageNumber)

	def GatherAnime(self, pageCount):
		html = self.SplitToListOfHtmls(self.html)
		crawlerRegexQuery = [r'<a\shref(?:[^\>])+>\s*(?P<AnimeName>[^\<]+)', r'<a\shref="(?P<Link>[^\"]+)']

		kissParser = KissParser('https://kissanime.ru/MyList/1132864')
		self.kissParsers.append(kissParser)
		Debug.Log('[KissCrawler] Trying to connect to ', str('http://kissanime.ru/AnimeList?page=' + str(pageCount)))
		kissParser.GetListOfKissAnimeEntities(crawlerHtmls=html, crawlerRegexQuery=crawlerRegexQuery)

	def CrawlForAnime(self):
		pageCount = 0
		while True:
			# if pageCount == 1:
			# 	self.CleanUp()
			response = ScrapeHtml(str(str('http://kissanime.ru/AnimeList?page=' + str(pageCount))), scraper=self.scraper)

			if response is not None and len(RemoveHtmlTrash(str(response.content))) > 250:
				
				if response.status_code != 200 or self.ContainsNotFound(RemoveHtmlTrash(str(response.content))):
					self.CleanUp()
					break;
			
				crawler = KissCrawler(html=RemoveHtmlTrash(str(response.content)), crawledPageNumber=pageCount)
				crawler.start()
				self.crawlers.append(crawler)
				time.sleep(1.5)
			else:
				Debug.Log('[KissCrawler] Something went wrong url=', str('http://kissanime.ru/AnimeList?page=' + str(pageCount)), '\nHTML:\n', RemoveHtmlTrash(str(response.content)), '\n')
				pageCount += 1
				continue

			if pageCount % 30 == 0 and pageCount > 0:
				self.CleanUp()
			
			pageCount += 1	

	def CleanUp(self):
		Debug.Log('[KissCrawler] Periodical cleanup...')
		areAlive = True
		while areAlive:
			areAlive = False
			for crawler in self.crawlers:
				if crawler.isAlive():
					areAlive = True
					time.sleep(2)

		for crawler in self.crawlers:
			for kissParser in crawler.kissParsers:
				kissParser.SyncWithDatabase()	

		for crawler in self.crawlers:
			crawler.join(0.5)		

		self.crawlers = []

	def SplitToListOfHtmls(self, html):
		listOfHtmls = regex.split(r'(?:<tr>.+?<td)|(?:<tr\sclass=\"odd\")()', html)
		listOfHtmls = list(filter(None, listOfHtmls))
		return listOfHtmls[1:]

	def ContainsNotFound(self, html):
		regexResult = regex.findall(r'(Not\sfound)', RemoveHtmlTrash(html))
		if len(regexResult) == 1:
			return True
		else:
			return False
