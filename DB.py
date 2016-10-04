import sqlite3, atexit
from Utils import *

class DB():
	db = None
	@staticmethod
	def GetDB():
		if DB.db is None:
			DB.db = DB()
		return DB.db

	def __init__(self):
		self.db = sqlite3.connect('anime.db')
		self.cursor = self.db.cursor()

		self.cursor.execute('SELECT name FROM sqlite_master WHERE type = "table"')
		if self.cursor.fetchone() is None:
			self.cursor.execute("CREATE TABLE KissAnime(AnimeName TEXT PRIMARY KEY, Synonyms TEXT, EpisodeCount INT, UserState TEXT, AnimeID INT)")
			self.cursor.execute("CREATE TABLE MalAnime(AnimeName TEXT, Synonyms TEXT, EpisodeCount INT, UserState TEXT, AnimeID INT PRIMARY KEY)")
			Debug.Log('Database created @ /anime.db')
		else:
			Debug.Log('Loaded existing database from /anime.db')

	def GetKissAnimeEntityCount(self):
		self.cursor.execute('SELECT COUNT(*) FROM KissAnime')
		return self.cursor.fetchone()[0]
	def GetMalAnimeEntityCount(self):
		self.cursor.execute('SELECT COUNT(*) FROM MalAnime')
		return self.cursor.fetchone()[0]

	def AddKissAnimeEntities(self, animeEntities):
		for animeEntity in animeEntities:
			self.AddKissAnimeEntity(animeEntity)
	def AddMalAnimeEntities(self, animeEntities):
		for animeEntity in animeEntities:
			self.AddMalAnimeEntity(animeEntity)
	def AddKissAnimeEntity(self, animeEntity):
		self.cursor.execute('INSERT INTO KissAnime VALUES(?, ?, ?, ?, ?)', self.ParseToTuple(animeEntity))
	def AddMalAnimeEntity(self, animeEntity):
		self.cursor.execute('INSERT INTO MalAnime VALUES(?, ?, ?, ?, ?)', self.ParseToTuple(animeEntity))

	def GetKissAnimeEntities(self, animeName=None, animeId=None):
		animeEntities = []
		
		if animeName is None and animeId is None:
			Debug.Log('[DB] animeName = ', animeName, ' animeId = ', animeId, ' are unsupported parameters')
			return None

		self.cursor.execute('SELECT * FROM KissAnime WHERE AnimeName LIKE ? AND AnimeID LIKE ? OR AnimeName LIKE ? AND AnimeID IS NULL', (animeName if animeName is not None else '%', animeId  if animeId is not None else '%', animeName if animeName is not None else '%'))			
		values = self.cursor.fetchall()

		Debug.Log('Length of values ', str(len(values)))

		if len(values) == 0:
			return None

		for value in values:
			Debug.Log(value)

		for value in values:
			animeEntity = self.ParseToAnimeEntity(value)
			animeEntities.append(animeEntity)
		return animeEntities
	def GetMalAnimeEntities(self, animeName=None, animeId=None):
		animeEntities = []
		
		if animeName is None and animeId is None and origin is None:
			Debug.Log('[DB] animeName = ', animeName, ' animeId = ', animeId, ' are unsupported parameters')
			return None

		self.cursor.execute('SELECT * FROM MalAnime WHERE AnimeName LIKE ? AND AnimeID LIKE ?', (animeName if animeName is not None else '%', animeId  if animeId is not None else '%'))			
		values = self.cursor.fetchall()

		if len(values) == 0:
			return None

		for value in values:
			animeEntity = self.ParseToAnimeEntity(value)
			animeEntities.append(animeEntity)
		return animeEntities

	def GetMalAnimeEntityByKissAnimeEntity(self, animeEntity):
		self.cursor.execute('''
			SELECT m.AnimeName, m.Synonyms, m.EpisodeCount, k.UserState, m.AnimeID
			FROM MalAnime as m
			JOIN KissAnime as k
			ON m.AnimeName = k.AnimeName AND k.AnimeName LIKE ?
			''', (str('%' + animeEntity.animeName + '%'), ))
		values = self.cursor.fetchall()

		if len(values) == 0:
			return None

		if len(values) == 1:
			return self.ParseToAnimeEntity(values)

		animeEntities = []
		for value in values:
			animeEntities.append(self.ParseToAnimeEntity(value))

		return self.GetBestMatchingMalAnime(animeEntity, animeEntities)

	def ParseToAnimeEntity(self, values):
		animeEntity = AnimeEntity(values[0], list(filter(lambda x: x != '', values[1].split(';'))), values[2], IdentifyUserState(values[3]), values[4])
		return animeEntity
	def ParseToTuple(self, animeEntity):
		values = ()
		values += (animeEntity.animeName if animeEntity.animeName is not None else None, )
		values += (';'.join(animeEntity.synonyms) if animeEntity.synonyms is not None else None, )
		values += (animeEntity.episodeCount if animeEntity.episodeCount is not None else None, )
		values += (animeEntity.userState.name if animeEntity.userState is not None else None, )
		values += (animeEntity.animeId if animeEntity.animeId is not None else None, )
		return values

	def GetAllKissAnimeEntities(self):
		self.cursor.execute('SELECT * FROM KissAnime')
		animeEntities = []
		for value in self.cursor.fetchall():
			animeEntity = self.ParseToAnimeEntity(value)
			animeEntities.append(animeEntity) 
		return animeEntities
	def GetAllMalAnimeEntities(self):
		self.cursor.execute('SELECT * FROM MalAnime')
		animeEntities = []
		for value in self.cursor.fetchall():
			animeEntity = self.ParseToAnimeEntity(value)
			animeEntities.append(animeEntity) 
		return animeEntities

	def GetBestMatchingMalAnime(self, kissAnimeEntitie, malAnimeEntities):
		for malAnimeEntity in malAnimeEntities:
			if kissAnimeEntitie.animeName == malAnimeEntity.animeName:
				return malAnimeEntity
			for malSynonym in malAnimeEntity.synonyms:
				if kissAnimeEntitie.animeName == malSynonym:
					return malAnimeEntity
				for kissSynonym in kissAnimeEntitie.synonyms:
					if kissSynonym == malSynonym:
						return malAnimeEntity
		return None

	def SaveAndCloseDB(self):
		Debug.Log('Database closed.')
		self.db.commit()
		self.db.close()

atexit.register(DB.GetDB().SaveAndCloseDB)