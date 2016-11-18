import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from VideoScraper import *
from VideoLinkScraperThread import *

from kivy.lang import Builder
from kivy.uix.videoplayer import VideoPlayer

class MyApp(App):

	def build(self):
		scraper = VideoScraper.GetVideoScraper()
		thread = VideoLinkScraperThread('http://kissanime.to/Anime/Haikyuu-Third-Season/Episode-005?id=131750', scraper)
		thread.start()
		while thread.isAlive():
			time.sleep(1)
		print(thread.videoLinks) 
		print('loading ', thread.videoLinks[0][0])
		player = VideoPlayer(source=thread.videoLinks[0][0], state='play',options={'allow_stretch': True})
		return player
        

if __name__ == '__main__':
    MyApp().run()
