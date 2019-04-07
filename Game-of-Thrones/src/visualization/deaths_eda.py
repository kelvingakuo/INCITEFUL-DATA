# Computations for vizes involving deaths. From /data/interim/all_deaths_sn1_sn6.csv

import pandas as pd
import re

pd.options.mode.chained_assignment = None



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
	def __init__(self, deathsPath, charsPath, levelPath):
		""" Creates dataframes from deaths, all characters, and character level CSV files
		"""
		self.deathsDF = pd.read_csv(deathsPath)
		self.charsDF = pd.read_csv(charsPath)
		self.levelDF = pd.read_csv(levelPath)



	def whenDeathsOccur(self):
		""" Slice and dice the data for visualisation purposes about death timings
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
		epInfo.drop(['episode_id', 'defined_death'], inplace = True, axis = 1)
		self.ep_with_most_deaths = epInfo# Plot the timeline of death. Somehow

	

	def waysToDie(self):
		""" Slice and dice the data for visualisation purposes about causes of death
		"""
		definedDeaths = self.deathsDF[self.deathsDF['defined_death'] == 1][['cause_of_death', 'perpetrator']]
		otherDeaths = self.deathsDF[self.deathsDF['defined_death'] == 0][['cause_of_death', 'perpetrator']] # Deaths not split into 'cause & perpetrator'

		definedDeaths['cause_of_death'] = definedDeaths['cause_of_death'].astype(str).str.lower()
		definedDeaths['cause_of_death'] = definedDeaths['cause_of_death'].replace({'kill': 'killed'})


		# 1. Cause of death e.g. most die, suicide etc
		definedDeaths['death_count'] = definedDeaths.groupby(['cause_of_death'])['cause_of_death'].transform('size')
		definedDeaths.drop_duplicates(['cause_of_death'], keep='first', inplace=True)
		definedDeaths.drop(['perpetrator'], inplace = True, axis = 1)
		definedDeaths.sort_values('death_count', inplace = True, ascending = False)

		otherDeaths['death_count'] = 1
		otherDeaths.drop(['perpetrator'], inplace = True, axis = 1)

		totalDeathCount = pd.concat([definedDeaths, otherDeaths])
		self.ways_to_die = totalDeathCount # **********Plot ways to die. Comment on most gruesome way(s) to die
		
		# 2. Who kills the most i.e. frequent perpetrator
		killed = self.deathsDF[self.deathsDF['cause_of_death'] == 'killed'][['cause_of_death', 'perpetrator']]
		killed['death_count'] = killed.groupby(['perpetrator'])['perpetrator'].transform('size')
		killed.drop_duplicates(['perpetrator'], keep='first', inplace=True)
		killed.drop(['cause_of_death'], inplace = True, axis = 1)
		killed.sort_values('death_count', inplace = True, ascending = False)
		self.killers = killed # **********Plot murderers

	
	def charBookFeatureVsDeath(self):
		""" Slice and dice the data for visualisation purposes about character features vs death, as per the book features
		"""
		#deadBookDF = self.charsDF.loc[self.charsDF['alive'] == 0] # Those dead in the books
		#deadShowDF = self.deathsDF # Those dead on the show

		# Too many nulls on the deadBookDF. Viable columns: male[0 | 1], book1[0 | 1], book2, book3, book4, book5, married[0 | 1], nobility, number_of_dead_relations

		self.relationWithGender = self.charsDF[['alive', 'male']]
		self.relationWithBook1 = self.charsDF[['alive', 'book1']]
		self.relationWithBook2 = self.charsDF[['alive', 'book2']]
		self.relationWithBook3 = self.charsDF[['alive', 'book3']]
		self.relationWithBook5 = self.charsDF[['alive', 'book5']]
		self.relationWithMarital = self.charsDF[['alive', 'married']]
		self.relationWithRelations = self.charsDF[['alive', 'number_of_dead_relations']]



	def charLevelVsDeath(self):
		""" Slice and sice the data for visualisation purposes about chararacter level (main vs supporting) vs death
		"""
		#print(self.levelDF)
		#print(self.deathsDF)

		self.deadCharLevelDF = self.deathsDF.merge(self.levelDF, on = 'name')




