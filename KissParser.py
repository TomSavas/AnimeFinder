from Utils import *
import SearchThread

class KissParser():
	def __init__(self, kissBookmarkUrl=None):
		self.kissBookmarkUrl = kissBookmarkUrl if kissBookmarkUrl is not None else GetKissBookmarkListUrlFromUser()
		self.searchThreads = []
		self.animeEntities = []

	def GetBookmarkListOfHtmls(self, kissBookmarkUrl=None):
		kissBookmarkUrl = self.kissBookmarkUrl if kissBookmarkUrl is None else kissBookmarkUrl

		html = GetHtml(kissBookmarkUrl)
		listOfHtmls = regex.split(r'class="trAnime', html)
		listOfHtmls = list(filter(None, listOfHtmls))
		return listOfHtmls[1:]

	def GetEntityInfo(self, html, searchThreads=None):
		searchThreads = self.searchThreads if searchThreads is None else searchThreads

		animeEntity = KissAnimeEntity()
		
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
		listOfHtmls = self.GetBookmarkListOfHtmls()

		for html in listOfHtmls:
			animeEntity = self.GetEntityInfo(html)
			if animeEntity is None : continue
			self.animeEntities.append(animeEntity)
			
		for thread in self.searchThreads:
			if thread.isAlive():
				Debug.Log('Gathering data...')
				time.sleep(5)

		for (animeEntity, thread) in zip(self.animeEntities, self.searchThreads):
			animeEntity.episodeCount = thread.episodeCount
			animeEntity.synonyms = thread.synonyms

		for thread in self.searchThreads:
			thread.join()

		return self.animeEntities
