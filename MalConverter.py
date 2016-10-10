import base64
import requests
import re as regex
from HtmlParsing import *


class MalConverter():
	def __init__(self, name, password, animeInfo=None):
		self.authHeader = self.GetHttpAuthHeader(name, password)
		if animeInfo is None:
			animeInfo, _, __ = getAnimeInfo()
			self.animeInfo = animeInfo[1:]
		else:
			self.animeInfo = animeInfo

	def GetHttpAuthHeader(self, name, password):
		credentials = name + ':' + password
		authToken = str(ToBase64(str.encode(credentials)))[2:-1]
		authHeader = {'Authorization' : str('Basic ' + authToken)}
		return authHeader
	def GetUserXml(self):
		xml = requests.get('https://myanimelist.net/api/account/verify_credentials.xml', headers=self.authHeader).text
		user_id = '<user_id>' + regex.search(r'<id>(?P<user_id>\d+)', xml).group('user_id') + '</user_id>'
		user_name = '<user_name>' + regex.search(r'<username>(?P<user_name>[^<]+)', xml).group('user_name') + '</user_name>'
		user_export_type = '<user_export_type>1</user_export_type>'
		properXml = user_id + '\n' + user_name + '\n' + user_export_type + '\n'
		return properXml

	def ListOfSearchReturnsFromMalInXml(self, animeName):
		animeName = animeName.replace(' ', '+')
		searchUrl = 'https://myanimelist.net/api/anime/search.xml?q=' + animeName
		response = requests.get(searchUrl, headers=self.authHeader)

		splitXml = regex.split(r'(?:<entry>)|(?:</entry>)', response.text)
		animeXmlList = []	
		for i in splitXml:
			if '<title>' in i:
				animeXmlList.append(i)
		return animeXmlList
	def AnimeXmlToListOfDicts(self, animeXmlList):
		animeFromMalList = []
		for i in animeXmlList:
			animeInfo = {'State': '', 'AnimeName': '', 'EpisodeCount': 0, 'Id': 0}
			animeInfo['Id'] = regex.search(r'<id>(?P<Id>\d+)</id>', i).group('Id')
			animeInfo['AnimeName'] = regex.search(r'<title>(?P<AnimeName>[^<]+)</title>', i).group('AnimeName')
			animeInfo['EpisodeCount'] = int(regex.search(r'<episodes>(?P<EpisodeCount>\d+)</episodes>', i).group('EpisodeCount'))
			animeInfo['State'] = regex.search(r'<status>(?P<State>[^<]+)</status>', i).group('State')
			animeFromMalList.append(animeInfo)
		return animeFromMalList
	def GetAnimeFromMalAsListOfDicts(self, animeName):
		animesXmlList = self.ListOfSearchReturnsFromMalInXml(animeName)
		animeFromMalAsListOfDicts = self.AnimeXmlToListOfDicts(animesXmlList)
		return animeFromMalAsListOfDicts
	def GetAnimeFromMal(self, animeName):
		animeFromMalAsListOfDicts = self.GetAnimeFromMalAsListOfDicts(animeName)

		targetAnime = ''
		for i in self.animeInfo:
			if animeName.lower() in i['AnimeName'].lower():
				targetAnime = i

		possible = []
		for i in animeFromMalAsListOfDicts:
			if targetAnime['AnimeName'].lower() in i['AnimeName'].lower() or i['AnimeName'].lower() in targetAnime['AnimeName'].lower():
				possible.append(i)
		if len(possible) == 1:
			return possible[0], targetAnime

		minimum = -1
		anime = ''
		for i in possible:
			if minimum == -1:
				minimum = abs(targetAnime['EpisodeCount'] - i['EpisodeCount'])
				anime = i
			elif abs(targetAnime['EpisodeCount'] - i['EpisodeCount']) < minimum:
				minimum = abs(targetAnime['EpisodeCount'] - i['EpisodeCount'])
				anime = i

		return anime, targetAnime

	def AnimeToExportXml(self, animeFromMal, animeFromKiss):
		series_animedb_id = '<series_animedb_id>' + animeFromMal['Id'] + '</series_animedb_id>'
		my_status = '<my_status>' + 'Completed' if animeFromKiss['IsWatched'] else 'Plan to Watch' + '</my_status>'   
		update_on_import = '<update_on_import>1</update_on_import>'
		xml = '<anime>\n' + series_animedb_id + '\n' + my_status + '\n' + update_on_import + '\n' + '</anime>\n'
		return xml

	def GetExportXml(self):
		userXml = self.GetUserXml()
		animeXmls = []
		for i in self.animeInfo:
			animeFromMal, animeFromKiss = self.GetAnimeFromMal(i['AnimeName'])
			print('animeFromMal:', animeFromMal)
			print('animeFromKiss:', animeFromKiss)
			animeXmls.append(self.AnimeToExportXml(animeFromMal, animeFromKiss))

		xml = '<?xml version="1.0" encoding="UTF-8" ?>\n'
		xml += '<!--\nCreated by MalConverter\nProgrammed by Savas\n-->'
		xml += '<myanimelist>\n'
		xml += userXml
		for i in animeXmls:
			xml += i
		xml += '</myanimelist>'

		return xml

def ToBase64(credentials):
	encoded = base64.b64encode(credentials)
	return encoded


# animeInfo, _, __ = getAnimeInfo()
converter = MalConverter('TomSavas', 'Oppaidaisuki')
# anime = converter.GetAnimeFromMal('Kill la Kill')
# print(anime)
print(converter.GetExportXml())