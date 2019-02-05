import scrapy
from scrapy.exceptions import CloseSpider
import json
import time
import random

class GetKickstarterItems(scrapy.Spider):
	name = 'kickstarteritems'
	baseURL ="https://www.kickstarter.com/discover/advanced?google_chrome_workaround&woe_id=0&sort=magic&seed=%07d&page=%05d"%(2547000, 00001)
	start_urls = [baseURL]

#https://www.kickstarter.com/discover/advanced?google_chrome_workaround&woe_id=0&sort=magic&seed=2547000&page=00001
	def parse(self, response):
		currentPage = response.url
		pageNumber = int(currentPage[-5:]) #Extract page number as last 5 chars on the URL
		currentSeed =  int(currentPage[-18:-11])#Seed is 7 chars, 11th from last char
		
		data = json.loads(response.body)
	
		for project in data.get('projects', []): #Parse project JSON
			item = dict()
			#Project Details
			item['projectId'] = project.get('id')
			item['projectName'] = project.get('name')
			item['blurb'] = project.get('blurb')
			item['goal'] = project.get('goal')
			item['pledged'] = project.get('pledged')
			item['state'] = project.get('state')
			item['deadline'] = project.get('deadline')
			item['launch'] = project.get('launched_at')
			item['backers'] = project.get('backers_count')
			item['currency'] = project.get('currency')

				#Creator details
			item['creatorId'] = project.get('creator', {}).get('id')
			item['creatorName'] = project.get('creator', {}).get('name')

				#Location details
			item['country'] = project.get('location', {}).get('country')

				#Category details
			item['categoryId'] = project.get('category', {}).get('id')
			item['categoryName'] = project.get('category', {}).get('name')	

			yield item

	
		if (data['has_more']):
			
			if(pageNumber==200):
				nxt = 1
				var = random.randint(1, 100)
				seed = currentSeed + var #Increment by a random value
				if(seed <= 2548000):
					getNxtJSON = "https://www.kickstarter.com/discover/advanced?google_chrome_workaround&woe_id=0&sort=magic&seed=%07d&page=%05d"%(seed, nxt)
					time.sleep(600) #Sleep for 10 minutes before using the next seed from page 1
					yield scrapy.Request(url=getNxtJSON , callback=self.parse)
				else: #Enough seeds, stop!!
					raise CloseSpider('ENOUGH DATA. TIME FOR CLEANING!!!')
		
			else:
				nxt = pageNumber + 1
				seed = currentSeed
				getNxtJSON = "https://www.kickstarter.com/discover/advanced?google_chrome_workaround&woe_id=0&sort=magic&seed=%07d&page=%05d"%(seed, nxt)
				time.sleep(5) #Sleep for five seconds then go to the next page
				yield scrapy.Request(url=getNxtJSON , callback=self.parse)
