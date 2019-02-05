# -*- coding: utf-8 -*-
import scrapy
import time

class LyricsbotSpider(scrapy.Spider):
	name = 'lyricsbot'
	start_urls = ['http://www.metrolyrics.com/drake-lyrics.html', 'http://www.metrolyrics.com/kanye-west-lyrics.html', 'http://www.metrolyrics.com/kendrick-lamar-lyrics.html', 'http://www.metrolyrics.com/j-cole-lyrics.html', 'http://www.metrolyrics.com/migos-lyrics.html', 'http://www.metrolyrics.com/jay-z-lyrics.html', 'http://www.metrolyrics.com/eminem-lyrics.html', 'http://www.metrolyrics.com/nicki-minaj-lyrics.html', 'http://www.metrolyrics.com/lil-wayne-lyrics.html', 'http://www.metrolyrics.com/future-lyrics.html', 'http://www.metrolyrics.com/dr-dre-lyrics.html', 'http://www.metrolyrics.com/nas-lyrics.html', 'http://www.metrolyrics.com/cardi-b-lyrics.html', 'http://www.metrolyrics.com/rick-ross-lyrics.html', 'http://www.metrolyrics.com/lil-yachty-lyrics.html', 'http://www.metrolyrics.com/wiz-khalifa-lyrics.html']

	def parse(self, response):
		songs = response.css('div#popular div.content table.songs-table tbody tr')
		artist = response.css('div.artist-header div.grid_6 h1::text').extract_first()

		for song in songs:
			item = dict()
			item['artist'] = artist
			item['name'] = song.css('td:nth-child(n+1) a::text').extract_first()
			item['link'] = song.css('td:nth-child(n+1) a::attr(href)').extract_first()
			link = item['link']
			item['year'] = song.css('td:nth-child(n+3)::attr(content)').extract_first()
			

			request = scrapy.Request(url=link, callback=self.parseLyrics)
			request.meta['item'] = item
			yield request			

		next = response.css('p.pagination a.next::attr(href)').extract_first()
		if (next is not None):
			time.sleep(30)
			yield response.follow(next, self.parse)


	def parseLyrics(self, response):
		item = response.meta['item']

		item['lyric'] = ''.join(response.css('div.lyrics-body div#lyrics-body-text p.verse::text').extract())
		yield item

