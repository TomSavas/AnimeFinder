from Debug import *
from UserState import *

class AnimeEntity:
	def __init__(self, animeName=None, synonyms=None, episodeCount=None, userState=None):
		self.animeName = animeName
		self.synonyms = synonyms
		self.episodeCount = episodeCount
		self.userState = userState 

	def Log(self):
		animeEntityAsString = ''
		for var in vars(self).keys():
			animeEntityAsString += str(str(var) + '=' + str(vars(self)[var]) + '\n\t\t\t    ')
		Debug.Log(animeEntityAsString)

	def Print(self):
		animeEntityAsString = ''
		for var in vars(self).keys():
			animeEntityAsString += str(str(var) + '=' + str(vars(self)[var]) + '\n\t\t\t    ')
		Debug.Print(animeEntityAsString)

class KissAnimeEntity(AnimeEntity):
	def __init__(self, animeName=None, synonyms=None, episodeCount=None, userState=None):
		super().__init__(animeName, synonyms, episodeCount, userState)
		self.originSite = 'Kissanime'

class MalAnimeEntity(AnimeEntity):
	def __init__(self, animeName=None, synonyms=None, episodeCount=None, userState=None, animeId=None):
		super().__init__(animeName, synonyms, episodeCount, userState)
		self.animeId = animeId
		self.originSite = 'MAL'
