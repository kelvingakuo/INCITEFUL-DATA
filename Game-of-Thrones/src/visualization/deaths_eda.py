# Vizes involving deaths. From /data/interim/all_deaths.csv

import matplotlib.pyplot as plt
import pandas as pd
import re
import seaborn as sns


sns.set(style='whitegrid')




# Killed by
# WHen deaths occur i.e. episode and time e.g. episode with most deaths
# Do main chars or supporting chars die
# Character feature e.g. nobility, gender vs death
#


class DeathsEDA(object):
	def __init__(self, deathsPath, charsPath, episodesPath):
		self.deathsDF = pd.read_csv(deathsPath)
		self.charsDF = pd.read_csv(charsPath)
		

		

	def whenDeathsOccur(self):
		pass

		





if __name__ == '__main__':
	deathsCSV = '../../data/interim/all_deaths.csv'
	charsCSV = '../../data/interim/character_features.csv'


	vizes = DeathsEDA(deathsCSV, charsCSV)
	vizes.whenDeathsOccur()