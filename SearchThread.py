from Utils import *

class SearchThread(threading.Thread):

	def __init__(self, html, crawlerRegexQuery=None):
		threading.Thread.__init__(self)
		self.html = html
		self.episodeCount = 0
		self.synonyms = []
		self.crawlerRegexQuery = crawlerRegexQuery

	def run(self):
		self.episodeCount = self.GetEpisodeCount()
		self.synonyms = self.GetAnimeSynonyms()
		
	def GetAnimeHtml(self):
		url = 'http://kissanime.to'
		try:
			if self.crawlerRegexQuery is None:
				regexResult = regex.search(r'"aAnime"\shref="(?P<Link>/Anime/[^"]+)\"\>(?P<AnimeName>[^<]+)', self.html)
			else:
				regexResult = regex.search(self.crawlerRegexQuery, self.html)

			url += regexResult.group('Link')
		except Exception as exception:
			Debug.Log(traceback.format_exc())
			return None

		html = ScrapeHtml(url)
		html = RemoveHtmlTrash(str(html.content)) if html is not None else ''  
		return html

	def GetEpisodeCount(self):
		html = self.GetAnimeHtml()
		if html is None:
			self.episodeCount = 0
			return self.episodeCount

		try:
			html = regex.split(r'\<table\sclass\=\"listing\"\>', html)
			if len(html) <= 1:
				self.episodeCount = 0
				return 0

			html = regex.split(r'\<\/table\>', html[1])[0]
			regexQuery = '<a\s+?href.*?()'
			regexResult = regex.findall(regexQuery, html)
			self.episodeCount = len(regexResult)
		except Exception as exception:
			Debug.Log(traceback.format_exc(), html)
			self.episodeCount = 0

		return self.episodeCount
	def GetAnimeSynonyms(self):
		html = self.GetAnimeHtml()

		synonyms = []
		try:
			html = regex.split(r'<p>\s+?<span', html)
			if len(html) < 2:	
				return synonyms
			html = html[1] 
			html = regex.split(r'Genres', html)[0]
			synonyms = regex.findall(r'(?:title.+?">([^<]+))', html)
		except Exception as exception:
			Debug.Log(traceback.format_exc(), html)

		for synonym in synonyms:
			if not IsHexInString(synonym):
				self.synonyms.append(synonym.replace('\\', ''))
		return self.synonyms