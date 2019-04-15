# Vizes involving deaths as per deaths_eda.py

import matplotlib.pyplot as plt
import seaborn as sns


from deaths_eda import DeathsEDA


sns.set(style='darkgrid')

def createTitleAndLabel(title, xLbl, yLbl, xLim = None, yLim = None):
	plt.title(title, weight = 'bold', fontsize = 15, y = 1.03)
	plt.xlabel(xLbl, weight = 'bold')
	plt.ylabel(yLbl, weight = 'bold')
	plt.xlim(xLim, None)
	plt.ylim(yLim, None)

class DeathsVizes(DeathsEDA):
	def __init__(self, deathsPath, charsPath, levelPath):
		DeathsEDA.__init__(self, deathsPath, charsPath, levelPath)

	def vizwhenDeathsOccur(self):
		"""Visualise computations done in whenDeathsOccur()
		"""
		self.whenDeathsOccur()
		#sns.lineplot(x = 'season', y = 'deaths_per_season', data = self.seasonal_deaths)
		#createTitleAndLabel('GoT NUMBER OF DEATHS PER SEASON', 'Season', 'Number of deaths', 0, 0)
		#plt.show()

		#sns.barplot(x = 'time_range', y = 'deaths_per_range', data = self.minutal_deaths)
		#createTitleAndLabel('GoT WHEN DEATHS OCCUR IN AN EPISODE', 'Time', 'Number of deaths')
		#plt.show()

		# self.episodal_deaths

		# S06E10 had most deaths at 11 deaths. Here is a breakdown...
		print(self.ep_with_most_deaths)


	def vizwaysToDie(self):
		"""Visualise computations done in waysToDie()
		"""
		self.waysToDie()
		# self.ways_to_die
		# self.killers


	def vizcharFeatureVsDeath(self):
		"""Visualise computations done in charFeatureVsDeath()
		"""
		self.charFeatureVsDeath()
		#self.relationWithGender
		#self.relationWithBook1
		#self.relationWithBook2
		#self.relationWithBook3
		#self.relationWithBook5
		#self.relationWithMarital
		#self.relationWithRelations


	def vizcharLevelVsDeath(self):
		""" Visualise computations done in charLevelVsDeath()
		"""
		self.charLevelVsDeath()
		# self.deadCharLevelDF



if __name__ == '__main__':
	deathsCSV = '../../data/interim/all_deaths_sn1_sn6.csv'
	charsCSV = '../../data/raw/character_attrs.csv'
	levelCSV = '../../data/raw/character_level.csv'


	vizes = DeathsVizes(deathsCSV, charsCSV, levelCSV)
	vizes.vizwhenDeathsOccur()
