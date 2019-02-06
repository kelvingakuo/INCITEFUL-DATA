import os
import pandas as pd
import sys

from winners import Winners 
from audio_features import Features

from songs_and_artists import main as getSongData
from run_crawlers import runCrawler

from log_config import logger


def parseData(data):
	""" Write raw data to CSV file 
	"""
	j = 0
	while j < len(data['type']):
		fileName = data['type'][j]
		dictdata = data['data'][j]

		fil = '../../data/raw/' + fileName + '.csv'
		df = pd.DataFrame.from_dict(dictdata, orient = 'columns')

		df.to_csv(fil, index = False, encoding = 'utf-8')
		j = j + 1


def dataFromSource(param):
	""" Return a dict or list of artist and/ or song information
	"""
	newArtist = pd.read_csv('../../data/interim/best_new_artist.csv')
	recordOfYear = pd.read_csv('../../data/interim/record_of_the_year.csv')
	songOfYear = pd.read_csv('../../data/interim/song_of_the_year.csv')

	if(param == 'artists'):
		info = getSongData('artistsOnly')

	else:
		info = getSongData('songsAndArtists')

	return info



def main(choice):
	if(choice == 'song_winners'):
		obj = Winners(['song', 'record']) #1. Extract best song and best record
		data = obj.bestRecordsAndSongs()
		parseData(data)

	elif(choice == 'artist_winners'):
		obj = Winners(['artist']) #2. Extract best new artist
		data = obj.bestNewArtist()
		parseData(data)

	elif(choice == 'lyrics'):
		logger.info('Generating records and songs files for the crawler...')
		items = dataFromSource('songs')
		logger.info('Records and Songs files generated!!')

		runCrawler('lyrics') #3. Run Scrapy lyrics extractor

	elif(choice == 'artist_data'):
		logger.info('Generating list of artists for the crawler...')
		artists = dataFromSource('artists')
		logger.info('List of artists generated!!')

		runCrawler('artistData') #4. Run Scrapy artist data extractor

	elif(choice == 'audio_features'):
		obj = Features()

		songs = dataFromSource('songs')
		# Implement Features() to get track ID and audio features where possible

	elif(choice == 'aa'):
		print(os.getcwd())

	




	else:
		print('Wrong input. Try again!!!')
		sys.exit()

	







if __name__ == "__main__":
	main(sys.argv[1])
