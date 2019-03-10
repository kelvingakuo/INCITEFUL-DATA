# Vizes involving deaths. From /data/interim/all_deaths_sn1_sn6.csv

import matplotlib.pyplot as plt
import pandas as pd
import re
import seaborn as sns


sns.set(style='whitegrid')
pd.options.mode.chained_assignment = None



# Killed by
# Do main chars or supporting chars die
# Character feature e.g. nobility, gender vs death
#

def nonExistentEpisode(ls):
	""" Return the episode lacking per season
	Input: ls - List of episodes in season
	"""
	fullEps = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	lacking = set(fullEps) - set(ls)
	return lacking


class DeathsEDA(object):
	def __init__(self, deathsPath, charsPath):
		self.deathsDF = pd.read_csv(deathsPath)
		self.charsDF = pd.read_csv(charsPath)




	def whenDeathsOccur(self):
		""" Slice and dice the data for visualisation purposes
		"""
		# 1. Deaths per season
		seasons = self.deathsDF[['season']]
		seasons['deaths_per_season'] = seasons.groupby(['season'])['season'].transform('size')
		seasons.drop_duplicates(['season'], keep='first', inplace=True) 
		seasons.sort_values('deaths_per_season', ascending = False, inplace = True) 
		self.seasonal_deaths = seasons # **********Plot deaths per seasons

		# 2. Deaths per episode
		episodes = self.deathsDF[['episode_id', 'season', 'episode', 'episode_name']]
		episodes['deaths_per_episode'] = episodes.groupby(['episode_id'])['episode_id'].transform('size')
		episodes.drop_duplicates(['episode_id'], keep='first', inplace=True) 
		episodes.drop(['episode_id'], inplace = True, axis = 1)
		episodes.sort_values('deaths_per_episode', ascending = False, inplace = True) 
		self.episodal_deaths = episodes # **********Plot deaths per episodes

		# 3. Break down of timings of deaths
		minutes = self.deathsDF[['minute']]
		earliest = minutes.min() # **********Talk about earliest death
		latest = minutes.max() # **********Talk about latest death

		bins = [0, 10, 20, 30, 40, 50, 60]
		labels = ["0 to 10 minutes", "10 to 20 minutes", "20 to 30 minutes", "30 to 40 minutes", "40 to 50 minutes", "50 to 60 minutes"]
		minutes['time_range'] = pd.cut(minutes['minute'], bins=bins, labels=labels, right=False)
		minutes['deaths_per_range'] = minutes.groupby(['time_range'])['time_range'].transform('size')
		minutes.drop_duplicates(['time_range'], keep='first', inplace=True)
		minutes.drop(['minute'], inplace = True, axis = 1)
		minutes.sort_values('deaths_per_range', ascending = False, inplace = True) 
		self.minutal_deaths = minutes # **********Plot deaths per time range
		

		# 4. Episodes without deaths
		deaths = episodes[['season']]
		deaths['episodes_per_season'] = deaths.groupby(['season'])['season'].transform('size')
		deaths.drop_duplicates(['season'], keep='first', inplace=True)
		deaths.sort_values('season', inplace = True, ascending = False)
		notFull = deaths.loc[deaths['episodes_per_season'] < 10]['season'].tolist() #Get seasons without deaths

		df = self.deathsDF.loc[self.deathsDF['season'].isin(notFull)][['episode', 'season']]
		fd = df.groupby(['season']).apply(lambda f: f['episode'].unique()) #Find episode lacking in the seasons
		rd = pd.DataFrame({'season': fd.index, 'episodes': fd.values})

		rd['missing_episode'] = rd['episodes'].apply(lambda r: nonExistentEpisode(r)) # **********Talk about no deaths in these episodes


		# 5. Breakdown of deaths for highest deaths episode
		mostDeaths = episodes.iloc[0]
		epName = mostDeaths.episode_name
		epInfo = self.deathsDF.loc[self.deathsDF['episode_name'] == epName] # DF of info about episode with most deaths

		
	

	def vizDeathsTimes(self):
		"""Visualise computations done in whenDeathsOccur()
		"""
		self.whenDeathsOccur()
		# self.seasonal_deaths
		# self.episodal_deaths
		# self.minutal_deaths



		





if __name__ == '__main__':
	deathsCSV = '../../data/interim/all_deaths_sn1_sn6.csv'
	charsCSV = '../../data/interim/character_features.csv'


	vizes = DeathsEDA(deathsCSV, charsCSV)
	vizes.vizDeathsTimes()