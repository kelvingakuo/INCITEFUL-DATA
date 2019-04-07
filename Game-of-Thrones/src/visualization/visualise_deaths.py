# Vizes involving deaths as per deaths_eda.py

import matplotlib.pyplot as plt
import seaborn as sns


from deaths_eda import DeathsEDA


sns.set(style='whitegrid')

class DeathsVizes(DeathsEDA):
	def __init__(self, deathsPath, charsPath, levelPath):
		DeathsEDA.__init__(self, deathsPath, charsPath, levelPath)

	def vizwhenDeathsOccur(self):
		"""Visualise computations done in whenDeathsOccur()
		"""
		self.whenDeathsOccur()
		sns.lineplot(x = 'season', y = 'deaths_per_season', data = self.seasonal_deaths)
		plt.show()

		# self.episodal_deaths
		# self.minutal_deaths
		# self.ep_with_most_deaths


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
