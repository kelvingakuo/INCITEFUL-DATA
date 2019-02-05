# Extract list of winners from the Grammys website
from bs4 import	BeautifulSoup
import datetime
import re
import requests
import random


def getNameAndYear(header):
	match = re.search(r'(.*)  \((.*)\)' , header, re.I|re.M)
	name = match.group(1)
	year = match.group(2)

	return name, year

def partialContent(url):
	content = requests.get(url).content
	soup = BeautifulSoup(content, 'html.parser')

	title = soup.find('div', class_ = 'sub-title').text.encode('ascii','ignore').decode('ascii')
	fileName = title.strip().replace(' ', '_').replace('/','_').lower()

	grammys = soup.find_all('div', class_ = 'view-grouping')

	return soup, fileName, grammys



class Winners:
	def __init__(self, category = None):
		self.baseURL = 'https://www.grammy.com/grammys/awards/winners-nominees/{}'
		self.song = []
		self.artist = []

		if(category is not None):
			if('record' in category):
				self.song.append(138)
			if('song' in category):
				self.song.append(140)
			if('artist' in category):
				self.artist.append(141)
		else:
			self.song = [138, 140]
			self.artist = [141]


	def bestRecordsAndSongs(self):
		"""Hit the endpoints and return data as dict.
		This function is for best record and best song winners only!!
		"""
		data = dict()
		data['id'] = []
		data['ceremony'] = []
		data['year'] = []
		data['artist'] = []
		data['song'] = []

		allData = []
		allFiles = []

		for point in self.song:
			url = self.baseURL.format(point)

			soup, fileName, grammys = partialContent(url) #1

			for grammy in grammys:
				header = grammy.find('div', class_ = 'view-grouping-header').text.encode('ascii','ignore').decode('ascii')
				ceremony, year = getNameAndYear(header) #2

				if((int(year) + 1) == int(datetime.date.today().year)): # Hack to avoid collecting current nominees
					continue
				else:
					content = grammy.find('div', class_ = 'wrapper views-fieldset')

					song = content.find('h4', class_ = 'field-content').text.encode('ascii','ignore').decode('ascii').strip() #3
					artist = content.find('a', class_ = 'freelink freelink-nid freelink-internal')
					if(artist is None):
						artist = content.find('div', class_ = 'field-content')

					artist = artist.text.encode('ascii','ignore').decode('ascii').strip() #4

					data['ceremony'].append(ceremony)
					data['year'].append(year)
					data['artist'].append(artist)
					data['song'].append(song)
					data['id'].append(random.randint(0,1500000))

			allData.append(data)
			allFiles.append(fileName)

			data = dict()
			data['id'] = []
			data['ceremony'] = []
			data['year'] = []
			data['artist'] = []
			data['song'] = []


		returned = {'type': allFiles, 'data': allData}
		
		return returned



	def bestNewArtist(self):
		"""Hit the endpoints and return data as dict.
		This function is for top new artists only!!
		"""
		data = dict()
		data['id'] = []
		data['ceremony'] = []
		data['year'] = []
		data['artist'] = []

		allData = []
		allFiles = []

		for point in self.artist:
			url = self.baseURL.format(point)
			
			soup, fileName, grammys = partialContent(url) #1

			for grammy in grammys:
				header = grammy.find('div', class_ = 'view-grouping-header').text.encode('ascii','ignore').decode('ascii')
				ceremony, year = getNameAndYear(header) #2

				if((int(year) + 1) == int(datetime.date.today().year)):
					continue
				else:
					artist = grammy.find('div', class_ = 'view-grouping-content').find('div', class_ ='views-field views-field-title').text.encode('ascii','ignore').decode('ascii')

				data['ceremony'].append(ceremony)
				data['year'].append(year)
				data['artist'].append(artist)
				data['id'].append(random.randint(0,1500000))

			allData.append(data)
			allFiles.append(fileName)

			data = dict()
			data['id'] = []
			data['ceremony'] = []
			data['year'] = []
			data['artist'] = []

		returned = {'type': allFiles, 'data': allData}

		return returned




		