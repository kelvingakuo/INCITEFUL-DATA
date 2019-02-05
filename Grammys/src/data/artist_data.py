# Extract info about artists from Wikipedia
from bs4 import	BeautifulSoup
import datetime
import logging
import re
import requests

from log_config import logger

lib = logging.getLogger('urllib3')
lib.setLevel(logging.CRITICAL)

class Artists(object):
	def __init__(self):
		self.baseURL = 'https://en.wikipedia.org/wiki/{}'


	def getArtistInfo(self, artists):
		artistInfo = dict()
		artistInfo['type'] = [] #Band or solo act
		artistInfo['birthday'] = []
		artistInfo['ethnicity'] = []
		artistInfo['birthplace'] = []
		artistInfo['career_start'] = []
		artistInfo['genres'] = []
		artistInfo['music_labels'] = []
		artistInfo['instruments_played'] = []


		for theArtist in artists:
			artist = theArtist.replace(' ', '_')
			url = self.baseURL.format(artist)

			logger.info(url)

			headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36'}


			res = requests.get(url, headers = headers)

			if(res.status_code == 200):
				#Page exists
				soup = BeautifulSoup(res.content, 'html.parser')
				bio = soup.select('table.infobox.vcard')


				if(bio is None):
					logger.error('NOT ARTIST PAGE: {} ___ {}'.format(url, res.status_code))
				elif((type(bio) is list) & (len(bio) > 0)):
					bio = bio[0]
					name = bio.find('div', class_ = 'nickname')

					if(name is not None):
						name = name.text.encode('ascii','ignore').decode('ascii')
						logger.info('_____________________ {}'.format(name))

					elif(name is None):
						name = bio.find('td', class_ = 'nickname')

						if(name is not None):
							name = name.text.encode('ascii','ignore').decode('ascii')
							logger.info('_____________________ {}'.format(name))

						else: # Probably a Band
							logger.info('NO DATA')
							continue

				else:
					logger.info('NO DATA')
					continue

				
			else:
				# Check that entry
				logger.error('NON-EXISTENT DATA: {} ___ {}'.format(url, res.status_code))




		data = {'type': 'artist_information', 'data': artistInfo}
		return data

		