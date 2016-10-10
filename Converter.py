from KissParser import *
from MalParser import *
from Utils import *

class Converter():
	def __init__(self):
		self.kissParser = KissParser()
		self.malParser = MalParser()

	def TransferKissToMal(self):
		Debug.Log('[Counter]Getting anime entities from Kissanime.com')
		self.kissParser.GetListOfKissAnimeEntities()
		# self.kissParser.CountTimeSpent()
		Debug.Log('[Counter]Transferring anime entities from Kissanime.com to MAL, this might take a while')
		# self.malParser.AddAnimeEntitiesToMalList(self.kissParser.animeEntities)
		# self.malParser.animeEntities = list(filter(None, self.malParser.animeEntities))
		# Debug.Log('[Counter]Printing malParser animeEntities')
		# Debug.Log(str(len(self.malParser.animeEntities)))
		# for animeEntity in self.malParser.animeEntities:
		# 	animeEntity.Log()

# testerrino
# ComeTheFuckOn159DAFUQ

converter = Converter()
converter.TransferKissToMal()