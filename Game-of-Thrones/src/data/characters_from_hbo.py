# Extract all characters according to https://www.hbo.com/game-of-thrones/cast-and-crew
from bs4 import	BeautifulSoup
import pandas as pd
import requests



def main():
	url = 'https://www.hbo.com/game-of-thrones/cast-and-crew'
	content = requests.get(url).content

	soup = BeautifulSoup(content, 'html.parser')

	allChars = soup.find_all('div', class_ = 'modules/Cast--castMember')

	hboChars = dict()
	hboChars['character_name'] = []
	hboChars['character_picture'] = []
	hboChars['played_by'] = []

	for char in allChars:
		name = char.find('span', class_ = 'components/ThumbnailWithText--primaryText').text.encode('ascii','ignore').decode('ascii').strip()
		actor = char.find('span', class_ = 'components/ThumbnailWithText--secondaryText').text.encode('ascii','ignore').decode('ascii').strip()
		picture = char.find('div', class_ = 'components/Thumbnail--thumbnail components/Thumbnail--circle components/Thumbnail--adaptive').find('img').get('src')
		link = 'https://hbo.com{}'.format(picture)

		hboChars['character_name'].append(name)
		hboChars['character_picture'].append(link)
		hboChars['played_by'].append(actor)



	charsDF = pd.DataFrame.from_dict(hboChars, orient = 'columns')
	hboCharsCSV = '../../data/raw/characters_and_actors.csv'


	with open(hboCharsCSV, 'w') as characters_and_actors:
		charsDF.to_csv(characters_and_actors, index = False)



if __name__ == '__main__':
	main()

