# Extract info about houses from https://gameofthrones.fandom.com/wiki/Game_of_Thrones_Wiki
import json
import logging
import pandas as pd
import requests
from bs4 import	BeautifulSoup




class GoTHouses(object):
	def __init__(self):
		url = 'https://gameofthrones.fandom.com/wiki/Game_of_Thrones_Wiki'
		content = requests.get(url).content
		self.soup = BeautifulSoup(content, 'html.parser')

	def getHouses(self):
		self.allCharacters = self.soup.find('div', class_ = 'WikiaSiteWrapper').find('header').find('nav').select('ul')[9]
		greatHouses = self.allCharacters.find_all('li', class_ = 'wds-dropdown-level-2')[4]

		housesList = greatHouses.find('ul', class_ = 'wds-list').find_all('a')

		self.houses = dict()
		self.houses['name'] = []
		self.houses['link'] = []

		for house in housesList:
			name = house.text.encode('ascii','ignore').decode('ascii').strip()
			link = 'https://gameofthrones.fandom.com{}'.format(house.get('href'))

			self.houses['name'].append(name)
			self.houses['link'].append(link)


	def extractHouseInfo(self):
		#self.getHouses() # Create houses' links

		self.houses = dict()
		self.houses['name'] = []
		self.houses['link'] = []
		self.houses['logo'] = []
		self.houses['house_information'] = []

		self.houses['name'].append('House Stark')
		self.houses['link'].append('https://gameofthrones.fandom.com/wiki/House_Stark')



		j = 0 #len(self.houses['name'])
		while(j < 1):
			house = self.houses['name'][j]
			link = self.houses['link'][j]
		
			# Extract info
			mash = requests.get(link).content
			houseData = BeautifulSoup(mash, 'html.parser')
			info = houseData.find('div', class_ = 'mw-content-text').find('aside')

			logo = info.find('figure').find('a').get('href')
			self.houses['logo'].append(logo)

			infoContents = info.findChildren('div') # Get all data available
			theData = dict()
			theData['data_type'] = []
			theData['content'] = []

			for content in infoContents:
				dataPresent = content.get('data-source')
				if(dataPresent is not None):
					theInfo = content.find('div', class_ = 'pi-data-value').findChildren()
					
					for anInf in theInfo:
						print(anInf)
						print('\n\n\n')


			#self.houses['house_information'].append(theData)


			j = j + 1


		#print(self.houses)


		






if __name__ == '__main__':
	obj = GoTHouses()
	obj.extractHouseInfo()