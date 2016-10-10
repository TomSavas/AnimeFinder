from Utils import *
from TransferThread import TransferThread

class MalParser():
	def __init__(self, name=None, password=None):
		if name is None or password is None:
			self.name, self.password = GetMalCredentialsFromUser()
		else: 
			self.name, self.password = name, password
		self.authHeader = self.GetHttpAuthHeader()
		self.transferThreads = []
		self.animeEntities = []
	
	def GetHttpAuthHeader(self):
		credentials = self.name + ':' + self.password
		authToken = str(ToBase64(str.encode(credentials)))[2:-1]
		authHeader = {'Authorization' : str('Basic ' + authToken)}
		return authHeader
		
	def AddAnimeEntityToMalList(self, animeEntity):
		# Debug.Log('[MalParser]Making new thread for anime named: ', animeEntity.animeName)
		transferThread = TransferThread(self.authHeader, animeEntity)
		self.transferThreads.append(transferThread)
		transferThread.start() 
	def AddAnimeEntitiesToMalList(self, animeEntities):
		Debug.Log('[MalParser]Creating threads...')
		for animeEntity in animeEntities:
			self.AddAnimeEntityToMalList(animeEntity)

		for transferThread in self.transferThreads:
			self.animeEntities.append(transferThread.possibleAnime)		

		Debug.Log('[MalParser]Waiting for threads to finish...')
		for transferThread in self.transferThreads:
			if transferThread.isAlive():
				time.sleep(5)
				Debug.Log('[MalParser]Waiting for threads to finish...')
				

		Debug.Log('[MalParser]Joining threads...')
		for transferThread in self.transferThreads:
			transferThread.join()		