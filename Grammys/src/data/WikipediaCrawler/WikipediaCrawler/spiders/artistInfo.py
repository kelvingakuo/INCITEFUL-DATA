# -*- coding: utf-8 -*-
import pickle
import scrapy
import logging


class ArtistinfoSpider(scrapy.Spider):
	name = 'artistInfo'


	def start_requests(self):
		self.topURL = 'https://en.wikipedia.org/wiki/{}'
	
		with open('../artists.pkl', 'rb') as ls:
			artists = pickle.load(ls)


		for artist in artists:
			theArtist = artist.replace(' ', '_')
			url = self.topURL.format(theArtist)

			req = scrapy.Request(url = url, callback = self.parse)
			yield req

	def parse(self, response):
		if((response.status != 400) | (response.status != 404)):
			bio = response.css('table.infobox.vcard')
			logging.info(type(bio))
		else:
			logging.error('NON-EXISTENT')





	''' The data
		artistInfo = dict()
		artistInfo['type'] = [] # If 'born' exists, solo. Else, band or sth
		artistInfo['birthday'] = []
		artistInfo['ethnicity'] = []
		artistInfo['birthplace'] = []
		artistInfo['career_start'] = []
		artistInfo['genres'] = []
		artistInfo['music_labels'] = []
		artistInfo['instruments_played'] = []
	'''
