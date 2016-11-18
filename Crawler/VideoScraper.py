from Utils import *
import cfscrape 

class VideoScraper():
	loginHeaders = {
	    'host': "kissanime.to",
	    'connection': "keep-alive",
	    'cache-control': "no-cache",
	    'origin': "http://kissanime.to",
	    'upgrade-insecure-requests': "1",
	    'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36",
	    'content-type': "application/x-www-form-urlencoded",
	    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	    'referer': "http://kissanime.to/Login",
	}
	loginHeadersInitialized = False
	scraper = None

	@staticmethod
	def CreateVideoScraper(username='Savickeinas', password='Savas4871'):
		scraper = cfscrape.create_scraper(episodeSearching=True)
		VideoScraper.GetHeaders(username, password, scraper)
		return scraper

	@staticmethod
	def GetVideoScraper(username = "Savickeinas", password = "Savas4871"):
		if VideoScraper.scraper is None:
			VideoScraper.scraper = VideoScraper.CreateVideoScraper(username, password)
		return VideoScraper.scraper

	@staticmethod
	def GetHeaders(username, password, scraperToUse=None, update=False):
		if scraperToUse is not None:
			scraper = scraperToUse
		elif VideoScraper.scraper is not None:
			scraper = VideoScraper.scraper
		else:
			scraper = VideoScraper.GetVideoScraper(username, password)
		if update:
			VideoScraper.loginHeadersInitialized = False

		if not VideoScraper.loginHeadersInitialized:
			initialres = scraper.get(url='http://kissanime.to')

			cfuid = regex.split(r';', initialres[0].headers['Set-Cookie'])[0]
			cfclearance = regex.split(r';', initialres[1].history[0].headers['Set-Cookie'])[0]

			cookie = cfuid + '; ' + cfclearance
			VideoScraper.loginHeaders['cookie'] = cfuid + '; ' + cfclearance
			log = VideoScraper.Login(scraper, username, password)
			newClearance = regex.split(r';', log[1].history[0].headers['Set-Cookie'])[0]
			VideoScraper.loginHeaders['cookie'] = cfuid + '; ' + newClearance
			newLog = VideoScraper.Login(scraper, username, password)		
			VideoScraper.loginHeadersInitialized = True

	@staticmethod
	def GetHtml(url, scraper):
		response = scraper.get(url)
		if type(response) is tuple:
			html = RemoveHtmlTrash(str(response[1].content))
		else:
			html = RemoveHtmlTrash(str(response.content))
		return html

	@staticmethod
	def Login(scraper, username, password):
		loginData = str('username=' + username + '&password=' + password + '&redirect=')
		
		response = scraper.request("POST", url='http://kissanime.to/Login', data=loginData, headers=VideoScraper.loginHeaders)
		if type(response) is tuple:
			html = RemoveHtmlTrash(str(response[1].content))
		else:
			html = RemoveHtmlTrash(str(response.content))
		return response

VideoScraper.GetVideoScraper()