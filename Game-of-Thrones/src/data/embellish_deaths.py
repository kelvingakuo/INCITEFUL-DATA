# Improve /data/raw/deaths_and_episodes_S01_S06.csv

import pandas as pd
import re

def splitCauseOfDeath(killedBy, pos):
	# ____ by ____ <cause_of_death by perpetrator>
	matches = re.match(r'(.*) by (.*)', killedBy, re.M|re.I)


	if(pos == 1):
		if(matches is None):
			return killedBy
		else:
			return matches.group(1)
	elif(pos == 2):
		if(matches is None):
			return killedBy
		else:
			return matches.group(2)
	elif(pos == 3):
		if(matches is None):
			return 0
		else:
			return 1


def main():
	deathsCSV = '../../data/raw/deaths_S01_S06.csv'
	episodesCSV = '../../data/raw/episodes_S01_S06.csv'
		
		
	deathsDF = pd.read_csv(deathsCSV)
	epsDF = pd.read_csv(episodesCSV)

	# Split time
	deathsDF['time'] = pd.to_datetime(deathsDF['time'], format = '%M:%S')
	deathsDF['minute'] = deathsDF['time'].dt.minute
	deathsDF['second'] = deathsDF['time'].dt.second

	# Get actual episode number from epsDF
	mergedDF = deathsDF.merge(epsDF, how = 'inner', on = 'episode_id')
	mergedDF.drop(['episode_id', 'time', 'season_id', 'link', 'name_y'], inplace= True, axis = 1)
	mergedDF.rename(columns = {'name_x': 'name', 'episode_number': 'episode'}, inplace = True)

	mergedDF['cause_of_death'] = mergedDF['killed_by'].apply(lambda x: splitCauseOfDeath(x, 1))
	mergedDF['perpetrator'] = mergedDF['killed_by'].apply(lambda y: splitCauseOfDeath(y, 2))
	mergedDF['defined_death'] = mergedDF['killed_by'].apply(lambda z: splitCauseOfDeath(z, 3)) # Checks whether death was split into 'cause' and 'perpetrator'

	mergedDF.drop(['killed_by'], inplace= True, axis = 1)


	processedCSV = '../../data/interim/all_deaths.csv'

	mergedDF.to_csv(processedCSV, index = False)


if __name__ == '__main__':
	main()
