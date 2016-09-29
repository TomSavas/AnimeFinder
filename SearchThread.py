from Utils import *

class SearchThread(threading.Thread):

	def __init__(self, html):
		threading.Thread.__init__(self)
		self.html = html
		self.episodeCount = 0
		self.synonyms = []

	def run(self):
		self.episodeCount = self.GetEpisodeCount()
		self.synonyms = self.GetAnimeSynonyms()
		
	def GetAnimeHtml(self):
		url = 'http://kissanime.to'
		try:
			regexResult = regex.search(r'"aAnime"\shref="(?P<Link>/Anime/[^"]+)\"\>(?P<AnimeName>[^<]+)', self.html)
			url += regexResult.group('Link')
		except Exception as exception:
			Debug.Log(traceback.format_exc())
			return None

		html = ScrapeHtml(url)
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
			html = regex.split(r'<p>\s+?<span', html)[1]
			synonyms = regex.findall(r'(?:title.+?">([^<]+))', html)
		except Exception as exception:
			Debug.Log(traceback.format_exc(), html)

		for synonym in synonyms:
			if not IsHexInString(synonym):
				self.synonyms.append(synonym.replace('\\', ''))
		return self.synonyms