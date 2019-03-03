# Create list of whether character is main or supporting as per https://en.wikipedia.org/wiki/List_of_Game_of_Thrones_characters

from bs4 import	BeautifulSoup
import pandas as pd
import pprint
import requests


def main():
	url = 'https://en.wikipedia.org/wiki/List_of_Game_of_Thrones_characters'
	content = requests.get(url).content

	soup = BeautifulSoup(content, 'html.parser')

	
	characters = dict()
	characters['name'] = []
	characters['level'] = []

	characterSoup = soup.find_all('table', class_ = 'wikitable')
	mainSoup = characterSoup[0]
	supportingSoup = characterSoup[1]


	main = [x.text.encode('ascii','ignore').decode('ascii').strip() for x in mainSoup.find_all('a')]
	supporting = [x.text.encode('ascii','ignore').decode('ascii').strip() for x in supportingSoup.find_all('a')]
	

	mainIds = [9, 11, 13, 16, 18, 21, 24, 27, 29, 32, 35, 38, 40, 43, 46, 48, 51, 54, 56, 58, 61,64, 66, 69, 71, 74, 79, 81, 83, 85, 87, 90, 93, 96, 98, 101, 103, 106, 108, 110, 112, 114]
	supportIds = [9, 11, 13, 15, 17, 19, 22, 25, 27, 29, 31, 33, 37, 39, 40, 42, 44, 46, 48, 50, 52, 54, 57, 60, 63, 65, 67, 70, 72, 74, 76, 78, 80, 82, 86, 88, 90]


	mainList = [main[i] for i in mainIds]

	interimSupport = [supporting[i] for i in supportIds]
	addSupport = ['Ros', 'Irri', 'Doreah', 'Little Sam', 'Olly']
	supportingList = interimSupport + addSupport
	


	for item in mainList:
		characters['name'].append(item)
		characters['level'].append('main')

	for item in supportingList:
		characters['name'].append(item)
		characters['level'].append('supporting')



	df = pd.DataFrame.from_dict(characters, orient = 'columns')
	levelCSV = '../../data/raw/character_level.csv'


	with open(levelCSV, 'w') as characters_level:
		df.to_csv(characters_level, index = False)




if __name__ == '__main__':
	main()