import cfscrape, time, traceback, threading 
import re as regex
from UserState import *
from AnimeEntities import *
from Debug import *

scraper = None

def KissToMal(kissAnimeEntity):
	malAnimeEntity = MalAnimeEntity(animeName=kissAnimeEntity.animeName, synonyms=kissAnimeEntity.synonyms, episodeCount=kissAnimeEntity.episodeCount, state=kissAnimeEntity.state, userState=kissAnimeEntity.userState) 
	return malAnimeEntity

def MalToKiss(malAnimeEntity):
	kissAnimeEntity = KissAnimeEntity(animeName=malAnimeEntity.animeName, synonyms=malAnimeEntity.synonyms, episodeCount=malAnimeEntity.episodeCount, state=malAnimeEntity.state, userState=malAnimeEntity.userState)
	return kissAnimeEntity

def GetKissBookmarkListUrlFromUser():
	return input('Input your Kissanime bookmark \"share with friends\" link: ')

def GetScraper():
	global scraper
	if scraper is None:
		scraper = cfscrape.create_scraper()
	return scraper 

def GetHtml(url, scraper=None):
	html = str(GetScraper().get(url).content)
	html = html.replace('\r', '').replace('\n', '').replace('\\r', '').replace('\\n', '')
	return html

def IsHexInString(string):
	hexa = []
	regexQuery = r'(\\x.{2})'
	hexa = regex.findall(regexQuery, string)

	if len(hexa) != 0:
		return True
	else:
		return False