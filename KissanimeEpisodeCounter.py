from HtmlParsing import *

animeInfo, totalEpisodeCount, totalWatchedEpisodeCount = getAnimeInfo()
for i in animeInfo:
	print(i)
print('Total episode count:', totalEpisodeCount)
print('Total Watched episode count:', totalWatchedEpisodeCount)
print('Which @25mins an episode averages to', int(totalWatchedEpisodeCount*25/60), 'h or', int(totalWatchedEpisodeCount*25/60/24), 'days of watch time.')
