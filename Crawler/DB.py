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
		self.db = sqlite3.connect('../anime.db')
		self.cursor = self.db.cursor()

		self.cursor.execute('SELECT name FROM sqlite_master WHERE type = "table"')
		if self.cursor.fetchone() is None:
			self.cursor.execute("CREATE TABLE KissAnime(AnimeName TEXT PRIMARY KEY, Synonyms TEXT, EpisodeCount INT, UserState TEXT, AnimeID INT, Genres TEXT, Synapse TEXT, Cover TEXT, EpisodePageLinks TEXT, EpisodeLinks TEXT)")
			Debug.Log('Database created @ ../anime.db')
		else:
			Debug.Log('Loaded existing database from ../anime.db')

	def GetKissAnimeEntityCount(self):
		self.cursor.execute('SELECT COUNT(*) FROM KissAnime')
		return self.cursor.fetchone()[0]

	def AddKissAnimeEntities(self, animeEntities):
		for animeEntity in animeEntities:
			self.AddKissAnimeEntity(animeEntity)
	def AddKissAnimeEntity(self, animeEntity, episodePageLinks=None):
		self.cursor.execute('INSERT INTO KissAnime VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', self.ParseToTuple(animeEntity, episodePageLinks))

	def UpdateKissAnimeEntity(self, animeEntity, episodePageLinks):
		self.cursor.execute('UPDATE KissAnime SET EpisodeCount = ?, UserState = ?, AnimeID = ?, EpisodePageLinks = ? WHERE AnimeName LIKE ?', self.ParseToTupleForUpdate(animeEntity, episodePageLinks))

	def GetKissAnimeEntities(self, animeName=None, animeId=None):
		animeEntities = []
		
		if animeName is None and animeId is None:
			Debug.Log('[DB] animeName = ', animeName, ' animeId = ', animeId, ' are unsupported parameters')
			return None

		self.cursor.execute('SELECT * FROM KissAnime WHERE AnimeName LIKE ? AND AnimeID LIKE ? OR AnimeName LIKE ? AND AnimeID IS NULL', (animeName if animeName is not None else '%', animeId  if animeId is not None else '%', animeName if animeName is not None else '%'))			
		values = self.cursor.fetchall()

		if len(values) == 0:
			return None
			
		for value in values:
			animeEntity = self.ParseToAnimeEntity(value)
			animeEntities.append(animeEntity)
		return animeEntities

	def ParseToAnimeEntity(self, values):
		animeEntity = AnimeEntity(values[0] if values[0] is not None else '', list(filter(lambda x: x != '', values[1].split(';'))) if values[1] is not None else [], values[2] if values[2] is not None else 0, IdentifyUserState(values[3]), values[4], list(filter(lambda x: x != '', values[5].split(';'))) if values[5] is not None else [], values[6], values[7], list(filter(lambda x: x != '', values[8].split(';'))) if values[8] is not None else [])
		return animeEntity
	def ParseToTuple(self, animeEntity, episodePageLinks=None):
		values = ()
		values += (animeEntity.animeName if animeEntity.animeName is not None else None, )
		values += (';'.join(animeEntity.synonyms) if animeEntity.synonyms is not None else None, )
		values += (animeEntity.episodeCount if animeEntity.episodeCount is not None else None, )
		values += (animeEntity.userState.name if animeEntity.userState is not None else None, )
		values += (animeEntity.animeId if animeEntity.animeId is not None else None, )
		values += (';'.join(animeEntity.genres) if animeEntity.genres is not None else None, )
		values += (animeEntity.synapse if animeEntity.synapse is not None else None, )
		values += (animeEntity.cover if animeEntity.cover is not None else None, )
		values += (';'.join(episodePageLinks if episodePageLinks is not None else []) if animeEntity.episodePageLinks != [] else None, )
		values += (';'.join(animeEntity.episodes) if animeEntity.episodes is not None else None, )
		return values
	def ParseToTupleForUpdate(self, animeEntity, episodePageLinks=None):
		values = ()
		values += (animeEntity.episodeCount if animeEntity.episodeCount is not None else None, )
		values += (animeEntity.userState.name if animeEntity.userState is not None else None, )
		values += (animeEntity.animeId if animeEntity.animeId is not None else None, )
		values += (';'.join(episodePageLinks) if episodePageLinks is not None else None, )
		values += (animeEntity.animeName if animeEntity.animeName is not None else None, )
		return values

	def GetAllKissAnimeEntities(self):
		self.cursor.execute('SELECT * FROM KissAnime')
		animeEntities = []
		for value in self.cursor.fetchall():
			animeEntity = self.ParseToAnimeEntity(value)
			animeEntities.append(animeEntity) 
		return animeEntities

	def SaveAndCloseDB(self):
		Debug.Log('Database closed.')
		self.db.commit()
		self.db.close()

atexit.register(DB.GetDB().SaveAndCloseDB)