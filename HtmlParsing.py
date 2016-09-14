import cfscrape
import time 
import re as regex
from SearchThread import SearchThread

def getScraper():
	return cfscrape.create_scraper()

def getHtml(url, scraper):
	html = str(scraper.get(url).content)
	html = html.replace('\r', '').replace('\n', '').replace('\\r', '').replace('\\n', '')
	return html

def getBookmarkList(url, scraper):
	html = getHtml(url, scraper)
	html = regex.split(r'class="trAnime', html)
	html = list(filter(None, html))
	return html

def getBookmarkLink():
	link = input('Input your Kissanime bookmark \"share with friends\" link: ')
	return link

def getElementInfo(html, count, threads, scraper):
	info = {'AnimeName' : '', 'IsWatched' : False, 'State' : '', 'EpisodeCount' : 0, 'AnimeCount' : 0}
	
	try:
		reg = regex.search(r'\"aAnime\".href(?:[^\>])+>\s*(?P<AnimeName>[^\<]+)', html)
		info['AnimeName'] = reg.group('AnimeName')
	except:
		return None, count

	try:
		reg = regex.search(r'(?P<State>(Completed)|(Not\syet\saired)|(Episode\s\d+))', html)
		info['State'] = 'Ongoing' if 'Episode' in reg.group('State') else reg.group('State')  
	except:
		pass
		
	try:
		reg = regex.search(r'display:\sinline.+?(?P<IsWatched>(Unwatched)|(Watched))', html)
		info['IsWatched'] = True if reg.group('IsWatched') == 'Watched' else False		
	except:
		pass

	if info['State'] == 'Ongoing':
		try:
			reg = regex.search(r'(Episode\s\d+)', html)
			reg = regex.search(r'\d+', reg.group(0))
			info['EpisodeCount'] = int(reg.group(0))
			searchThread = None
		except:
			pass
	else:
		searchThread = SearchThread(count, scraper, html)
		threads[count] = searchThread
		searchThread.start()

	info['AnimeCount'] = count
	count += 1
	return info, count

def getAnimeInfo():
	url = getBookmarkLink()
	scraper = getScraper()
	html = getBookmarkList(url, scraper)
	
	infoList = []
	threads = {}
	count = 0
	for i in range(len(html)):
		info, count = getElementInfo(html[i], count, threads, scraper)
		if info is None : continue
		infoList.append(info)
		
	for i in threads.keys():
		if threads[i].isAlive():
			print('Gathering data...')
			time.sleep(5)

	for i in range(len(infoList)):
		if i in threads.keys(): 
			infoList[i]['EpisodeCount'] = threads[i].episodeCount

	for i in threads.keys():
		threads[i].join()

	totalEpisodeCount = countEpisodes(infoList, False)
	totalWatchedEpisodeCount = countEpisodes(infoList)

	return infoList, totalEpisodeCount, totalWatchedEpisodeCount

def countEpisodes(infoList, Watched = True):
	totalEpisodeCount = 0
	for i in infoList:
		if Watched:
			if i['IsWatched']:
				totalEpisodeCount += i['EpisodeCount']
		else:
			totalEpisodeCount += i['EpisodeCount']

	return totalEpisodeCount
