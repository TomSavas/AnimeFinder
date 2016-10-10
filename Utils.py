import cfscrape, time, traceback, threading, requests, base64
import re as regex
from UserState import *
from AnimeEntities import *
from Debug import *
from DB import *
from urllib.parse import urlencode 

scraper = None

def GetKissBookmarkListUrlFromUser():
	return input('Input your Kissanime bookmark \"share with friends\" link: ')
def GetMalCredentialsFromUser():
	name = input('Input your MAL username: ')
	password = input('Input your MAL password: ')
	return name, password

def GetGlobalScraper():
	global scraper
	if scraper is None:
		scraper = cfscrape.create_scraper()
	return scraper 
def GetScraper():
	return cfscrape.create_scraper()

def ScrapeHtml(url, scraper=None, timesFailed=0):
	try:
		if scraper is None:
			response = GetGlobalScraper().get(url)
		else:
			response = scraper.get(url)
	except Exception as exception:
		if timesFailed > 20:
			Debug.Log('CFscrape screwed up... \n', traceback.format_exc())
			return None
		time.sleep(0.2)			
		response = ScrapeHtml(url, scraper, timesFailed+1)

	return response
	# try:
	# 	if scraper is None:
	# 		html = str(GetGlobalScraper().get(url).content)
	# 	else:
	# 		if crawler:
	# 			response = scraper.get(url)
	# 			return response
	# 		else:
	# 			html = str(scraper.get(url).content)			
	# except Exception as exception:
	# 	if timesFailed > 100:
	# 		Debug.Log('CFscrape screwed up... \n', traceback.format_exc())
	# 		return None
	# 	time.sleep(0.2)
	# 	if crawler:
	# 		html = ScrapeHtml(url, scraper, True)
	# 	html = ScrapeHtml(url, scraper, False)	
	# 	return html
	# html = RemoveHtmlTrash(html)
	# return html
def RemoveHtmlTrash(html):
	return html.replace('\r', '').replace('\n', '').replace('\\r', '').replace('\\n', '')
def GetRequest(url, headers=None):
	if headers is not None:
		return requests.get(url, headers=headers).text
	else:
		return requests.get(url).text
def PostRequest(url, headers=None, payload=None):
	headers['content-type'] = 'application/x-www-form-urlencoded'
	if payload is not None:
		return requests.post(url, headers=headers, data=payload)
	else:
		return requests.post(url, headers=headers)
		
def IsHexInString(string):
	hexa = []
	regexQuery = r'(\\x.{2})'
	hexa = regex.findall(regexQuery, string)

	if len(hexa) != 0:
		return True
	else:
		return False

def DictToUrl(dict):
	return urlencode(dict)
def StringToUrl(string):
	dict = {'':string}
	return DictToUrl(dict)[1:].replace(r'%2B', '+')
def ToBase64(credentials):
	encoded = base64.b64encode(credentials)
	return encoded