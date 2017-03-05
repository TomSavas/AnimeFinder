from Debug import *
from UserState import *

class AnimeEntity:
	def __init__(self, animeName=None, synonyms=None, episodeCount=None, userState=None, animeId=None, genres=None, synapse=None, cover=None, episodePageLinks=[], episodes=[]):
		self.animeName = animeName	
		self.synonyms = synonyms
		self.episodeCount = episodeCount
		self.userState = userState
		self.animeId = animeId
		self.genres = genres
		self.synapse = synapse
		self.cover = cover
		self.episodePageLinks = episodePageLinks
		self.episodes = episodes

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
