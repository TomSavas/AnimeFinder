from Utils import *
import SearchThread

class KissParser():
	def __init__(self, kissBookmarkUrl=None):
		self.kissBookmarkUrl = kissBookmarkUrl if kissBookmarkUrl is not None else GetKissBookmarkListUrlFromUser()
		self.totalEpisodeCount = 0
		self.searchThreads = {}
		self.animeEntities = []
		self.episodePageLinks = {}

	def GetBookmarkListOfHtmls(self, kissBookmarkUrl=None):
		kissBookmarkUrl = self.kissBookmarkUrl if kissBookmarkUrl is None else kissBookmarkUrl

		html = RemoveHtmlTrash(str(ScrapeHtml(kissBookmarkUrl).content))
		listOfHtmls = regex.split(r'class="trAnime', html)
		listOfHtmls = list(filter(None, listOfHtmls))
		return listOfHtmls[1:]

	def GetEntityInfo(self, html, searchThreads=None, crawlerRegexQuery=None):
		searchThreads = self.searchThreads if searchThreads is None else searchThreads

		animeEntity = AnimeEntity()
		searchThread = None

		if crawlerRegexQuery is None:
			try:
				regexResult = regex.search(r'\"aAnime\".href(?:[^\>])+>\s*(?P<AnimeName>[^\<]+)', html)
				animeEntity.animeName = regexResult.group('AnimeName')#.replace(' (Sub)', '').replace(' (Dub)', '').replace(' (TV)', '')
			except Exception as exception:
				Debug.Log('\n', traceback.format_exc(), '\nHtml:\n', html)
				return AnimeEntity()

			try:
				regexResult = regex.search(r'display:\sinline.+?(?P<State>(Unwatched)|(Watched))', html)
				animeEntity.userState = IdentifyKissUserState(regexResult.group('State'))		
			except:
				Debug.Log('\n', traceback.format_exc(), '\nHtml:\n', html)
				return animeEntity
			searchThread = SearchThread.SearchThread(html)
		else:
			try:
				regexResult = regex.search(crawlerRegexQuery[0], html)
				animeEntity.animeName = regexResult.group('AnimeName')#.replace(' (Sub)', '').replace(' (Dub)', '').replace(' (TV)', '')
			except Exception as exception:
				Debug.Log('\n', traceback.format_exc(), '\nHtml:\n', html)
				return AnimeEntity()			
			
			animeEntity.userState = UserState.NotDefined
			searchThread = SearchThread.SearchThread(html, crawlerRegexQuery[1])

		if '(Sub)' in animeEntity.animeName or '(Sub)' in animeEntity.animeName or '(Sub)' in animeEntity.animeName:
			searchThread.synonyms.append(animeEntity.animeName.replace(' (Sub)', '').replace(' (Dub)', '').replace(' (TV)', '')) 

		self.searchThreads[animeEntity] = searchThread
		searchThread.start()

		return animeEntity
	def GetListOfKissAnimeEntities(self, crawlerHtmls=None, crawlerRegexQuery=None):
		if crawlerHtmls is None:
			Debug.Log('[KissParser] Gathering /anime/bookmarklist html')
			listOfHtmls = self.GetBookmarkListOfHtmls() if crawlerHtmls is None else crawlerHtmls
		else:
			listOfHtmls = crawlerHtmls

		Debug.Log('[KissParser] Parsing to anime entities')
		for html in listOfHtmls:
			animeEntity = self.GetEntityInfo(html, crawlerRegexQuery=crawlerRegexQuery)
			if animeEntity is None : continue
			self.animeEntities.append(animeEntity)
		Debug.Log('[KissParser] Done parsing to anime entities, amount of entities = ', str(len(self.animeEntities)))

		Debug.Log('[KissParser] Waiting for threads to finish...')	
		areAlive = True
		while areAlive:
			areAlive = False
			for animeEntity in self.animeEntities:
				if self.searchThreads[animeEntity].isAlive():
					areAlive = True
					time.sleep(0.2)

		Debug.Log('[KissParser] Gathering episodeCount and synonyms...')			
		for animeEntity in self.animeEntities:
			searchThread = self.searchThreads[animeEntity]
			animeEntity.episodeCount = searchThread.episodeCount
			animeEntity.synonyms = searchThread.synonyms
			animeEntity.genres = searchThread.genres
			animeEntity.synapse = searchThread.synapse
			animeEntity.cover = searchThread.cover
			animeEntity.videoLinks = searchThread.videoLinks
			animeEntity.episodePageLinks = searchThread.episodePageLinks

			if animeEntity.animeName in self.episodePageLinks:
				self.episodePageLinks[animeEntity.animeName] += searchThread.episodePageLinks
			else:
				self.episodePageLinks[animeEntity.animeName] = searchThread.episodePageLinks

		Debug.Log('[KissParser] Joining threads..., total thread count = ', len(self.animeEntities))	
		for animeEntity in self.animeEntities:
			self.totalEpisodeCount += self.searchThreads[animeEntity].episodeCount
			self.searchThreads[animeEntity].join(0.5)
		# Debug.Log('[KissParser] Finished joining threads...')	

		if crawlerHtmls is None:
			Debug.Log('[KissParser] Syncing with database...')
			self.SyncWithDatabase()

	def SyncWithDatabase(self):
		for animeEntity in self.animeEntities:
			animeEntityFromDB = DB.GetDB().GetKissAnimeEntities(animeName=animeEntity.animeName)
			if animeEntityFromDB is not None:
				animeEntityFromDB = animeEntityFromDB[0] 
				if animeEntity.__dict__ != animeEntityFromDB.__dict__:
					if (animeEntity.episodeCount <= animeEntityFromDB.episodeCount or len(animeEntity.synonyms) <= len(animeEntityFromDB.synonyms)) and len(animeEntity.episodePageLinks) <= len(animeEntityFromDB.episodePageLinks):
						continue
					if animeEntity.animeName == animeEntityFromDB.animeName:
						Debug.Log('[KissParser] Found a missmatch animeName = ', animeEntity.animeName, ' updating in DB...\nanimeEntity: ', animeEntity.__dict__, '\nanimeEntityFromDB: ', animeEntityFromDB.__dict__)
						if animeEntity.animeName in self.episodePageLinks:
							DB.GetDB().UpdateKissAnimeEntity(animeEntity, self.episodePageLinks[animeEntity.animeName])
						else:
							DB.GetDB().UpdateKissAnimeEntity(animeEntity)
					else:
						Debug.Log('[KissParser] Found a missmatch animeName = ', animeEntity.animeName, ' adding to DB...\nanimeEntity: ', animeEntity.__dict__)
						DB.GetDB().AddKissAnimeEntity(animeEntity, self.episodePageLinks[animeEntity.animeName])
			else:
				Debug.Log('[KissParser] ', animeEntity.animeName, ' not found in DB, adding to DB...')
				DB.GetDB().AddKissAnimeEntity(animeEntity, self.episodePageLinks[animeEntity.animeName])

	def CountTimeSpent(self):
		episodeCount = 0
		for animeEntity in self.animeEntities:
			if animeEntity.userState.value == 2:
				episodeCount += animeEntity.episodeCount
		Debug.Log('You have watched ', episodeCount, ' which @25min rounds to ', str(int(episodeCount*25/60)), ' h or ', str(int(episodeCount*25/60/24)), 'days of watch time.')