# Extract info about deaths from deathtimeline.com
import json
import logging
import pandas as pd
import requests



def makeRequests(season, what):
	""" Get JSON data from this guy's API
	Input - Season as Int
		  - Data needed
	"""
	deathsURL = 'http://deathtimeline.com/api/deaths?season={}'
	epsURL = 'http://deathtimeline.com/api/seasons/{}/episodes'

	headers = {'Host':'deathtimeline.com', 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Mobile Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'}

	if(what == 'epInfo'):
		url = epsURL.format(season)
	elif(what == 'deathsInfo'):
		url = deathsURL.format(season)


	res = requests.get(url, headers = headers)
	data = json.loads(res.content)

	return data


def parseData(deathsData, epsData, season):
	""" Clean up and store data
	Input - Deaths and episodes data as dicts
	season as Int
	"""
	deathsDF = pd.DataFrame.from_dict(deathsData, orient = 'columns')
	epsDF = pd.DataFrame.from_dict(epsData, orient = 'columns')

	# Clean up deaths data
	deathsDF.drop(['id', 'importance', 'link', 'status', 'house'], axis = 1, inplace = True)
	deathsDF.rename(columns = {'killedBy': 'killed_by'}, inplace = True)
	deathsDF['season'] = season

	# Clean up episodes data
	epsDF.drop(['imdb', 'wiki'], axis = 1, inplace = True)
	epsDF.rename(columns = {'episodeNumber': 'episode_number', 'wikia': 'link', 'id': 
		'episode_id'}, inplace = True)
	

	if(season == 1):
		isHeaders = True
	else:
		isHeaders = False

	deathsCSV = '../../data/raw/deaths_s01_s06.csv'
	epsCSV = '../../data/raw/episodes_s01_s06.csv'


	with open(deathsCSV, 'a') as deaths, open(epsCSV, 'a') as eps:
		deathsDF.to_csv(deaths, index = False, header = isHeaders)
		epsDF.to_csv(eps, index = False, header = isHeaders)


	
def main():
	for i in range(1, 7):
		deaths = makeRequests(i, 'deathsInfo')
		episodes = makeRequests(i, 'epInfo')

		parseData(deaths, episodes, i)


if __name__ == '__main__':
	main()