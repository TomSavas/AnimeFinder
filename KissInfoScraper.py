from Utils import *
import SearchThread

class KissInfoScraper():
	def __init__(self):
		self.scraper = GetScraper()

	def GetInfoFromPage(self, url):
		response = ScrapeHtml(url=url, scraper=self.scraper)

		if response is None:
			return None
		else:
			animeEntity = AnimeEntity()
			html = RemoveHtmlTrash(str(response.content))

			# Debug.Log(html)

			# regexResult = regex.search(r'\"aAnime\".href(?:[^\>])+>\s*(?P<AnimeName>[^\<]+)', html)
			# animeEntity.animeName = regexResult.group('AnimeName').replace(' (Sub)', '').replace(' (Dub)', '').replace(' (TV)', '')

			animeEntity.userState = UserState.NotDefined
			searchThread = SearchThread.SearchThread(html, [r'<a\shref(?:[^\>])+>\s*(?P<AnimeName>[^\<]+)', r'<a\shref="(?P<Link>[^\"]+)'])
			searchThread.start() 

			time.sleep(5)

			animeEntity.synonyms = searchThread.synonyms
			animeEntity.EpisodeCount = searchThread.episodeCount

			animeEntity.Print()

			return animeEntity