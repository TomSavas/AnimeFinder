from Utils import *


class TransferThread(threading.Thread):
	def __init__(self, authHeader, animeEntity):
		threading.Thread.__init__(self)
		self.animeEntity = animeEntity
		self.authHeader = authHeader
		self.possibleAnime = ''

	def run(self):
		# Debug.Log('[TransferThread]Thread started')
		self.TransferAnime()
		# Debug.Log('[TransferThread]Thread end')

	def TransferAnime(self):
		possibleAnime = self.PickEquivalentToKissAnimeEntity(self.animeEntity)
		
		if possibleAnime is None:
			# Debug.Log('[TransferThread]Unable to find equivalent of ', self.animeEntity.animeName)
			self.possibleAnime = None
			return None
		self.possibleAnime = possibleAnime
		# payload = self.FormAddRequestXml(self.animeEntity)
		# payload = DictToUrl({'data':payload})
		# url = str('https://myanimelist.net/api/animelist/add/' + str(possibleAnime.animeId) + '.xml')
		# response = PostRequest(url, headers=self.authHeader, payload=payload)
		# if int(response.status_code) != 201:
		# 	Debug.Log('[TransferThread]Post request failed for ', self.animeEntity.animeName, ', response body:\n', response.text, ' \nPayload:\n', self.FormAddRequestXml(self.animeEntity), '\n', payload, '\nheaders = ', self.authHeader)

	def FindMalAnimeEntities(self, animeName):
		animeName = regex.sub(r'(?:[^\s\w]|[_])+', ' ', animeName)
		animeName = regex.sub(r'\s', '+', animeName)

		# Debug.Log('[TransferThread]Looking for anime by the name of ', animeName)

		url = 'https://myanimelist.net/api/anime/search.xml?q=' + animeName
		xmlResponse = GetRequest(url, self.authHeader)

		animeXmlList = []	
		for i in regex.split(r'(?:<entry>)|(?:</entry>)', xmlResponse):
			if '<title>' in i:
				animeXmlList.append(i)

		animeEntities = []
		for i in animeXmlList:
			animeEntity = AnimeEntity()
			animeEntity.animeId = regex.search(r'<id>(?P<animeId>\d+)</id>', i).group('animeId')
			animeEntity.animeName = regex.search(r'<title>(?P<animeName>[^<]+)</title>', i).group('animeName')
			animeEntity.episodeCount = int(regex.search(r'<episodes>(?P<episodeCount>\d+)</episodes>', i).group('episodeCount'))
			animeEntity.userState = UserState.PlanningToWatch

			synonyms = []
			for synonym in regex.findall(r'(?:(?:<synonyms>)|(?:<english>))([^<]+)(?:(?:</synonyms>)|(?:</english>))', i):
				if ';' in synonym:
					tmpSynonyms = regex.split(r'\s?;\s?', synonym)
					synonyms.extend(tmpSynonyms)
				elif ',' in synonym:
					tmpSynonyms = regex.split(r'\s?,\s?', synonym)
					synonyms.extend(tmpSynonyms)
				else:
					synonyms.append(synonym)
			animeEntity.synonyms = synonyms
			animeEntities.append(animeEntity)

		return animeEntities
	def PickEquivalentToKissAnimeEntity(self, kissAnimeEntity):
		possibleEquivalents = self.FindMalAnimeEntities(kissAnimeEntity.animeName)

		# Debug.Log('[TransferThread]Searching for ', kissAnimeEntity.animeName)
		
		for possibleAnimeEntity in possibleEquivalents:
			if possibleAnimeEntity.animeName.lower() == kissAnimeEntity.animeName.lower():
				# Debug.Log('[TransferThread]', possibleAnimeEntity.animeName.lower(), '==', kissAnimeEntity.animeName.lower(), 'True')
				return possibleAnimeEntity
			# Debug.Log('[TransferThread]', possibleAnimeEntity.animeName.lower(), '==', kissAnimeEntity.animeName.lower(), 'False')

			for possibleAnimeEntityName in possibleAnimeEntity.synonyms:
				for synonym in kissAnimeEntity.synonyms:
					if possibleAnimeEntityName.lower() == synonym.lower() or possibleAnimeEntityName.lower() == kissAnimeEntity.animeName.lower():
						# Debug.Log('[TransferThread]', possibleAnimeEntityName.lower(), '==', synonym.lower(), 'True')
						return possibleAnimeEntity
					# Debug.Log('TransferThread]', possibleAnimeEntityName.lower(), '==', synonym.lower(), 'False')

	def FormAddRequestXml(self, animeEntity):
		xml = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n'
		xml += '\t<entry>\n'
		xml += '\t\t<status>'
		xml += str(animeEntity.userState.value)
		xml += '</status>\n'
		xml += '\t</entry>\n'
		return xml			