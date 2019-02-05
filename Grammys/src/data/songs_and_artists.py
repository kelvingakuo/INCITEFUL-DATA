import os
import pandas as pd
import pickle
import json
import re

# Extract songs, and artists for use by the crawler


def getSongWriter(art):
	#print('Original: {}__________________'.format(art))
	match = re.match(r'(.*) songwriters((.*))', art, re.M|re.I)
	again = re.match(r'(.*) songwriter((.*))', art, re.M|re.I)
	if(match):
		artist = match.group(2)
		if(artist == '.'):
			artist = match.group(1)
		artist = ''.join(c for c in artist if c not in '(),.').lstrip()

	elif(again):
		artist = again.group(2)
		artist = ''.join(c for c in artist if c not in '(),.').lstrip()
	else:
		artist = art


	if('AND' in artist):
		new = re.match(r'(.*) AND ALSO (.*)', artist, re.M|re.I )
		artist = new.group(1)
	elif('&' in artist):
		new = re.match(r'(.*) & (.*)', artist, re.M|re.I )
		artist = new.group(1)
	elif('Featuring' in artist):
		new = re.match(r'(.*) Featuring (.*)', artist, re.M|re.I )
		artist = new.group(1)

	#print('Final: __________________________ {}'.format(artist))
	return artist


def main(what):
	"""Generate data for use by the lyrics crawler
	"""
	
	recs = pd.read_csv('../data/record_of_the_year.csv')
	sngs = pd.read_csv('../data/song_of_the_year.csv')
	arts = pd.read_csv('../data/best_new_artist.csv')

	records = dict()
	records['id'] = []
	records['song'] = []
	records['artist'] = []


	songs = dict()
	songs['id'] = []
	songs['song'] = []
	songs['artist'] = []



	j = 0

	while(j < len(recs['artist'])):
		records['id'].append(recs['id'].tolist()[j])
		records['song'].append(recs['song'].tolist()[j])
		records['artist'].append(recs['artist'].tolist()[j])

		songs['id'].append(sngs['id'].tolist()[j])
		songs['song'].append(sngs['song'].tolist()[j])
		artis = getSongWriter(sngs['artist'].tolist()[j])
		songs['artist'].append(artis)

		j = j + 1


	if(what == 'artistsOnly'):
		artists = records['artist'] + songs['artist'] + arts['artist'].tolist()
		info = sorted(list(set(artists)))

		return info

	else:
		if(os.path.exists('LyricsFreakCrawler/records.json') == False):
			with open('LyricsFreakCrawler/records.json', 'w') as pf:
				json.dump(records, pf)


			with open('LyricsFreakCrawler/songs.json', 'w') as fp:
				json.dump(songs, fp)