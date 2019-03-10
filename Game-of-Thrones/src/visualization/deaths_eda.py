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


class DeathsEDA(object):
	def __init__(self, deathsPath, charsPath):
		self.deathsDF = pd.read_csv(deathsPath)
		self.charsDF = pd.read_csv(charsPath)




	def whenDeathsOccur(self):
		seasons = self.deathsDF[['season']]
		seasons['deaths_per_season'] = seasons.groupby(['season'])['season'].transform('size')
		seasons.drop_duplicates(['season'], keep='first', inplace=True) 
		seasons.sort_values('deaths_per_season', ascending = False, inplace = True) # Deaths per season

		episodes = self.deathsDF[['episode_id', 'season', 'episode', 'episode_name']]
		episodes['deaths_per_episode'] = episodes.groupby(['episode_id'])['episode_id'].transform('size')
		episodes.drop_duplicates(['episode_id'], keep='first', inplace=True) 
		episodes.drop(['episode_id'], inplace = True, axis = 1)
		episodes.sort_values('deaths_per_episode', ascending = False, inplace = True) # Deaths per episode

		minutes = self.deathsDF[['minute']]
		earliest = minutes.min() # Earliest death
		latest = minutes.max() # Latest death

		





if __name__ == '__main__':
	deathsCSV = '../../data/interim/all_deaths_sn1_sn6.csv'
	charsCSV = '../../data/interim/character_features.csv'


	vizes = DeathsEDA(deathsCSV, charsCSV)
	vizes.whenDeathsOccur()