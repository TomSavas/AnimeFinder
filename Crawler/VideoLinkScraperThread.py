from Utils import *
from VideoScraper import *

class VideoLinkScraperThread(threading.Thread):
	def __init__(self, url, scraper):
		threading.Thread.__init__(self)
		self.url = url
		self.scraper = scraper
		self.name = ''
		self.videoLinks = []

	def run(self):
		self.GetName()
		self.GetLinks()

	def GetName(self):
		try:
			regexResult = regex.findall(r'/Anime/(.+?)\?', self.url)
			self.name = regexResult[0].replace('-', ' ').replace('/', ' ')
		except Exception as exception:
			Debug.Log(traceback.format_exc(), self.url)

	def GetLinks(self):
		# TODO: fix up cookie stuff, unable to reliably connect...
		html = VideoScraper.GetHtml(self.url, self.scraper)
		# Debug.Log('[VideoLinkScraper] name=', self.name, ' \nhtml=', html)	
		try:
				
			# regexResult = regex.findall(r'href="(.+?)">(\d{3,4}x\d{3,4}).mp4', html)
			captchaCheck = regex.findall(r'(Are\syou\shuman\?)', html)
			if len(captchaCheck) > 1:
				Debug.Log('[VideoLinkScraper] Captcha has been issued')
				return 
			regexResult = regex.findall(r'href="(https:\/\/.+?)".?(\d{3,4}x\d{3,4}).mp4', html)
			# Debug.Log('[VideoLinkScraper] name=', self.name, ' videoLinks=', regexResult, '\nhtml=', html)

			if len(regexResult) == 0:
				return

			# validatedLinks = []
			# for link in regexResult:
			# 	if len(regex.findall(r'google', link)) == 0:
			# 		validatedLinks.append(link)

			# self.videoLinks = validatedLinks
			
			self.videoLinks = regexResult
		except Exception as exception:
			Debug.Log(traceback.format_exc(), html)