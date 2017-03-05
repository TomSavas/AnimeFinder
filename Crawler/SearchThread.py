from Utils import *
import html

class SearchThread(threading.Thread):

	def __init__(self, html, crawlerRegexQuery=None):
		threading.Thread.__init__(self)
		self.html = html
		self.episodeCount = 0
		self.synonyms = []
		self.genres = []
		self.synapse = ''
		self.cover = ''
		self.episodePageLinks = []
		self.videoLinks = {}
		self.crawlerRegexQuery = crawlerRegexQuery

	def run(self):
		self.GetAnimeHtml()
		self.GetEpisodeCount()
		self.GetAnimeSynonyms()
		self.GetAnimeGenres()
		self.GetAnimeSynapse()
		self.GetCoverPicture()

	def GetAnimeHtml(self):
		url = 'http://kissanime.ru'
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
			return

		try:
			html = regex.split(r'\<table\sclass\=\"listing\"\>', self.html)
			if len(html) <= 1:
				self.episodeCount = 0
				return

			html = regex.split(r'\<\/table\>', html[1])[0]
			regexResult = regex.findall(r'<a.+?href="(.+?)"', html)
			self.episodeCount = len(regexResult)
			for link in regexResult:
				self.episodePageLinks.append(str('http://kissanime.ru' + link))
		except Exception as exception:
			Debug.Log(traceback.format_exc(), html)
			self.episodeCount = 0
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
	def GetAnimeGenres(self):
		genres = []
		try:
			genres = regex.findall(r'\/Genre\/(?P<Genres>[^"]+)', self.html)
		except Exception as exception:
			Debug.Log(traceback.format_exc(), self.html)
		self.genres = genres
	def GetAnimeSynapse(self):
		synapse = ''
		try:
			regexResult = regex.findall(r'Summary.+?(?:<.+?>)*(.+?)</p>', self.html)
			if len(regexResult) > 0:
				regexResult = regexResult[0]
				regexResult = regex.split(r'<.+?>', regexResult)
				regexResult = ''.join(regexResult)
				regexResult = regex.split(r'(\s){2,}', regexResult) 
				regexResult = ''.join(regexResult)
				regexResult = html.unescape(regexResult)
				synapse = regexResult.replace('\\', '')
		except Exception as exception:
			Debug.Log(traceback.format_exc(), self.html)
		self.synapse = synapse
	def GetCoverPicture(self):
		cover = ''
		try:
			regexResult = regex.findall(r'Cover.+?src="(.+?)"', self.html)
			if len(regexResult) > 0:
				cover = regexResult[0]
		except Exception as exception:
			Debug.Log(traceback.format_exc(), self.html)
		self.cover = cover