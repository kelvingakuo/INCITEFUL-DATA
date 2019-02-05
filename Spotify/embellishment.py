import os.path

import json
import pickle
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import random
import sys

from log_config import logger

def returnIds(a, b, c, d):
	r = a['id'].unique().tolist()
	s = b['id'].unique().tolist()
	t = c['id'].unique().tolist()
	u = d['id'].unique().tolist()

	ids = list(set(r + s + t + u))
	cleanIds = sorted([x for x in ids if str(x) != 'nan'])

	return cleanIds


def initSpotipy():
	clientId = '7164a28303d647bbb3dbe454d030b9ad'
	clientSecret = 'ebcf03cfaaab43b680a266aa9bbe3394'

	client_credentials_manager = SpotifyClientCredentials(client_id = clientId, client_secret = clientSecret)
	spotify = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
	spotify.trace=False

	return spotify

# Get the data from Spotify
def getAudioFeatures(i, spotify):
	logger.info('Getting audio features for {}'.format(i))
	features = spotify.audio_features(i)
	data = {i : features}
	return data

def getTrackInfo(i, spotify):
	logger.info('Getting track information for {}'.format(i))
	info = spotify.track(i)
	data = {i : info}
	return data



def main(startPoint):
	startPoint = int(startPoint)
	if(os.path.exists('data/unique_IDs.pkl') == False):

		a = pd.read_csv('data/top_200_daily.csv')
		a.dropna()
		b = pd.read_csv('data/top_200_weekly.csv')
		b.dropna()
		c = pd.read_csv('data/viral_50_daily.csv')
		c.dropna()
		d = pd.read_csv('data/viral_50_weekly.csv')
		d.dropna()

		uniqueIds = returnIds(a, b, c, d)

		with open('data/unique_IDs.pkl', 'wb') as i:
			pickle.dump(uniqueIds, i)

	
	if(os.path.exists('data/unique_IDs.pkl')):
		with open('data/unique_IDs.pkl', 'rb') as j:
			uniques = pickle.load(j)[startPoint:] 

		spotify = initSpotipy()

		j = startPoint
		for idef in uniques:
			features = getAudioFeatures(idef, spotify)
			info = getTrackInfo(idef, spotify)

			try:
				feats = []
				infs = []
				with open('data/audio_features.json', 'r') as feat, open('data/track_info.json', 'r') as inf:
					feats = json.load(feat)
					infs = json.load(inf)

				feats.append(json.dumps(features))
				infs.append(json.dumps(info))

				with open('data/audio_features.json', 'w') as feat, open('data/track_info.json', 'w') as inf:
					json.dump(feats, feat)
					logger.info('*******WROTE ITEM INDEX {} AUDIO FEATURE******'.format(j))
					json.dump(infs, inf)
					logger.info('*******WROTE ITEM INDEX {} TRACK INFO*****'.format(j))

				if(j%200 == 0):
					logger.info('Wrote {} objects'.format(j))
					n = j * 0.01
					t = random.randint(0, n)
					logger.debug('Sleeping for {} seconds'.format(t))
					time.sleep(t)
					spotify = initSpotipy()
				j = j + 1

			except IOError as e:
				logger.error(e)


		
		
if __name__ == "__main__":
	main(sys.argv[1])