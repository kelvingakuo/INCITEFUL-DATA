import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.options.mode.chained_assignment = None
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

sns.set(style='whitegrid')

def main():
	a = pd.read_csv('data/top_200_daily.csv')
	a.dropna()
	#b = pd.read_csv('data/top_200_weekly.csv')
	#b.dropna()
	#c = pd.read_csv('data/viral_50_daily.csv')
	#c.dropna()
	#d = pd.read_csv('data/viral_50_weekly.csv')
	#d.dropna()











if __name__ == "__main__":
	main()