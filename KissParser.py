from Utils import *
import SearchThread

class KissParser():
	def __init__(self, kissBookmarkUrl=None):
		self.kissBookmarkUrl = kissBookmarkUrl if kissBookmarkUrl is not None else GetKissBookmarkListUrlFromUser()
		self.totalEpisodeCount = 0
		self.searchThreads = []
		self.animeEntities = []

	def GetBookmarkListOfHtmls(self, kissBookmarkUrl=None):
		kissBookmarkUrl = self.kissBookmarkUrl if kissBookmarkUrl is None else kissBookmarkUrl

		html = ScrapeHtml(kissBookmarkUrl)
		listOfHtmls = regex.split(r'class="trAnime', html)
		listOfHtmls = list(filter(None, listOfHtmls))
		return listOfHtmls[1:]

	def GetEntityInfo(self, html, searchThreads=None):
		searchThreads = self.searchThreads if searchThreads is None else searchThreads

		animeEntity = AnimeEntity()
		
		try:
			regexResult = regex.search(r'\"aAnime\".href(?:[^\>])+>\s*(?P<AnimeName>[^\<]+)', html)
			animeEntity.animeName = regexResult.group('AnimeName').replace(' (Sub)', '').replace(' (Dub)', '').replace(' (TV)', '')
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
		self.searchThreads.append(searchThread)
		searchThread.start()

		return animeEntity
	def GetListOfKissAnimeEntities(self):
		Debug.Log('[KissParser]Gathering /anime/bookmarklist html')
		listOfHtmls = self.GetBookmarkListOfHtmls()

		Debug.Log('[KissParser]Parsing to anime entities')
		for html in listOfHtmls:
			animeEntity = self.GetEntityInfo(html)
			if animeEntity is None : continue
			self.animeEntities.append(animeEntity)
		Debug.Log('[KissParser]Done parsing to anime entities, amount of entities = ', str(len(self.animeEntities)))

		Debug.Log('[KissParser]Waiting for threads to finish...')	
		for thread in self.searchThreads:
			if thread.isAlive():
				time.sleep(5)

		Debug.Log('[KissParser]Gathering episodeCount and synonyms...')			
		for (animeEntity, thread) in zip(self.animeEntities, self.searchThreads):
			animeEntity.episodeCount = thread.episodeCount
			animeEntity.synonyms = thread.synonyms

		Debug.Log('[KissParser]Joining threads...')	
		for thread in self.searchThreads:
			self.totalEpisodeCount += thread.episodeCount
			thread.join()
		Debug.Log('[KissParser]Finished joining threads...')	

		Debug.Log('[KissParser]Syncing with database...')
		self.SyncWithDatabase()

	def SyncWithDatabase(self):
		for animeEntity in self.animeEntities:
			animeEntityFromDB = DB.GetDB().GetKissAnimeEntities(animeName=animeEntity.animeName)
			if animeEntityFromDB is not None:
				animeEntityFromDB = animeEntityFromDB[0] 
				print(animeEntity.__dict__)
				print(animeEntityFromDB.__dict__)
				if animeEntity.__dict__ != animeEntityFromDB.__dict__:
					Debug.Log('[KissParser]Found a missmatch animeName = ', animeEntity.animeName, ' adding to DB...')
					DB.GetDB().AddKissAnimeEntity(animeEntity)
			else:
				Debug.Log('[KissParser]', animeEntity.animeName, ' not found in DB, adding to DB...')
				DB.GetDB().AddKissAnimeEntity(animeEntity)

	def CountTimeSpent(self):
		episodeCount = 0
		for animeEntity in self.animeEntities:
			if animeEntity.userState.value == 2:
				episodeCount += animeEntity.episodeCount
		Debug.Log('You have watched ', episodeCount, ' which @25min rounds to ', str(int(episodeCount*25/60)), ' h or ', str(int(episodeCount*25/60/24)), 'days of watch time.')

	def CountTimeSpent(self):
		episodeCount = 0
		for animeEntity in self.animeEntities:
			if animeEntity.userState.value == 2:
				episodeCount += animeEntity.episodeCount
		Debug.Log('You have watched ', episodeCount, ' which @25min rounds to ', str(int(episodeCount*25/60)), ' h or ', str(int(episodeCount*25/60/24)), 'days of watch time.')