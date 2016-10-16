from Utils import *

class SearchThread(threading.Thread):

	def __init__(self, html, crawlerRegexQuery=None):
		threading.Thread.__init__(self)
		self.html = html
		self.episodeCount = 0
		self.synonyms = []
		self.genres = []
		self.summary = ''
		self.crawlerRegexQuery = crawlerRegexQuery

	def run(self):
		self.GetAnimeHtml()
		self.episodeCount = self.GetEpisodeCount()
		self.synonyms = self.GetAnimeSynonyms()
		self.genres = self.GetAnimeGenres()
		self.summary = self.GetAnimeSummary()

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
		self.html = html

	def GetEpisodeCount(self):
		if self.html is None:
			self.episodeCount = 0
			return self.episodeCount

		try:
			html = regex.split(r'\<table\sclass\=\"listing\"\>', self.html)
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
		synonyms = []
		try:
			html = regex.split(r'<p>\s+?<span', self.html)
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
	def GetAnimeGenres(self):
		genres = []
		try:
			genres = regex.findall(r'\/Genre\/(?P<Genres>[^"]+)', self.html)
		except Exception as exception:
			Debug.Log(traceback.format_exc(), self.html)
		return genres
	def GetAnimeSummary(self):
		summary = ''
		try:
			regexResult = regex.findall(r'Summary.+?(?:<.+?>)*(.+?)</p>', self.html)
			if len(regexResult) > 0:
				regexResult = regexResult[0]
				regexResult = regex.split(r'<.+?>', regexResult)
				regexResult = ''.join(regexResult)
				regexResult = regex.split(r'(\s){3,}', regexResult) 
				regexResult = ''.join(regexResult)
				regexResult = regex.split(r'(\&nbsp\;)', regexResult) 
				regexResult = ''.join(regexResult)
				regexResult = regex.split(r'(\&ldquo\;)', regexResult)
				regexResult = ''.join(regexResult)
				regexResult = regex.split(r'(\&rdquo\;)', regexResult) 
				summary = ''.join(regexResult)
		except Exception as exception:
			Debug.Log(traceback.format_exc(), self.html)
		return summary