# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import re


class LyricsfreakSpider(scrapy.Spider):
	name = 'lyricsfreak'

	def start_requests(self):
		self.topURL = 'https://www.lyricsfreak.com'
		self.baseURL = self.topURL+'/search.php?a=search&type=song&q={}&p={}' #Only the song is the argument

		with open('../records.json', 'r') as fp:
			self.records = json.load(fp)

		with open('../songs.json', 'r') as pf:
			self.songs = json.load(pf)


		start_urls = []
		compar = []
		ids = []
		theType = []

		k = 0
		while(k < len(self.records['song'])):
			songItem = self.songs['song'][k] # To search
			recordItem = self.records['song'][k]

			songI = self.songs['id'][k] # For storage
			recordI = self.records['id'][k]

			songFile = 'songs.json'
			recordFile = 'records.json'

			songArt = self.songs['artist'][k] # For comparison
			recordArt = self.records['artist'][k]



			songUrl = self.baseURL.format(songItem, 1)
			recordUrl = self.baseURL.format(recordItem, 1)	


			start_urls.append(songUrl)
			start_urls.append(recordUrl)

			compar.append(songArt)
			compar.append(recordArt)

			ids.append(songI)
			ids.append(recordI)	

			theType.append(songFile)
			theType.append(recordFile)	

			k = k + 1


		u = 0
		while(u < len(start_urls)):
			url = start_urls[u]

			comp = compar[u]
			idef = ids[u]
			fileType = theType[u]

			info = {'toComp': comp, 'id': idef, 'the_file': fileType}

			req = scrapy.Request(url = url, callback = self.parse)
			req.meta['info'] = info

			yield req

			u = u + 1



	def parse(self, response):
		metadata = response.meta['info']

		comparator = metadata['toComp']
		idef = metadata['id']
		theFile = metadata['the_file']

		results = response.xpath('//*[@id="cmn_wrap"]/div[4]/div[2]/div[1]/table/tbody/tr')

		for result in results:
			artist = result.css('td:nth-child(n+1) a::text').extract_first().strip()
			song = result.css('td:nth-child(n+2) a::attr(href)').extract_first()

			if(comparator in artist):  # If artist matches compar, follow link
				tryAgain = False
				lyricURL = self.topURL+song
				lyrRq = scrapy.Request(url = lyricURL, callback = self.getLyrics)
				lyrRq.meta['info'] = metadata

				yield lyrRq	
				break

				
				
			else: # Else, try all other pages of results
				tryAgain = True
				

		try:
			if(tryAgain):
				pgNo = int(response.url[-1:])
				nxt = str(pgNo + 1)
				tryAgainURL = re.sub(r'\d+$', nxt, response.url)

				tryReq = scrapy.Request(url = tryAgainURL, callback = self.parse)
				tryReq.meta['info'] = metadata

				yield tryReq	
		except UnboundLocalError: # This item needs to be checked manually
			logging.error('LYRICS NON-EXISTENT FOR THIS ITEM...')
			with open('try_another_lyric_search_term.txt', 'a') as tryFile:
				line = 'Retry for ITEM: {} ARTIST: {} in FILE: {}\n'.format(idef, comparator, theFile)
				tryFile.write(line)




	def getLyrics(self, response):
		metadata = response.meta['info']

		idef = metadata['id']
		theFile = metadata['the_file']


		theLyrics = response.xpath('//*[@id="content"]/text()').extract()

		item = dict()
		item['file'] = theFile
		item['id'] = idef
		item['lyrics'] = theLyrics

		yield item
