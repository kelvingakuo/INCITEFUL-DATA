import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
from wordcloud import WordCloud
from collections import Counter
import sys

sns.set(style='whitegrid')

def userCmpns(df):
	tf = pd.DataFrame({'creatorName': df['creatorName'].tolist()})
	tf['count'] = tf.groupby('creatorName')['creatorName'].transform('size')
	tf.drop_duplicates('creatorName', keep='first', inplace=True)
	sf = tf.sort_values('count', ascending=False)
	lbls = sf[0:3]['creatorName'].tolist()
	y = sf[0:3]['count'].tolist()	
	x = np.arange(len(y))

	plt.bar(x, y, color=['Green', 'Purple', 'Black'])
	plt.xticks(x, lbls)
	plt.xlabel('USER', fontsize=10)
	plt.ylabel('CAMPAIGNS', fontsize=10)
	plt.title('MOST ACTIVE USERS', fontsize=20)
	sns.set()
	plt.show()


def userSuccess(df):
	kf = pd.DataFrame({'creatorName': df['creatorName'], 'goal': df['goal'], 'pledged': df['pledged'], 'project': df['projectName']})
	kf['success'] = kf['pledged'] / kf['goal']
	sf = kf[kf['success'] >= 1] #Return only those successful
	sf['count'] = sf.groupby('creatorName')['creatorName'].transform('size')
	sf.drop_duplicates('creatorName', keep='first', inplace=True)
	gf = sf.sort_values('count', ascending=False)

	dd = sf.sort_values('success', ascending=False) #Sort by level of success
	
	lbls = gf[0:3]['creatorName'].tolist()
	y = gf[0:3]['count'].tolist()	
	x = np.arange(len(y))

	plt.bar(x, y, color=['#ff0000', '#008000', '#00FFFF'])
	plt.xticks(x, lbls)
	plt.xlabel('USER', fontsize=10)
	plt.ylabel('SUCCESSFUL CAMPAIGNS', fontsize=10)
	plt.title('MOST SUCCESSFUL USERS', fontsize=20)
	sns.set()
	plt.show()

	return lbls


''' Study the most successful user
def freedoms(topUsers, df):
	user = topUsers[0]
	fd = df.loc[df['creatorName'] == user]
	fd['success'] = fd['pledged'] / fd['goal']
	fd['categCount'] = fd.groupby('categoryName')['categoryName'].transform('size')
	

	succ= fd.sort_values('success', ascending=False) #Sorted by success
	monies = sum(fd['pledged']) #Total monies collected
	print(succ[0:1])

	return 0
'''

def forTableau(df): #Return count per country for Tableau viz
	fd = pd.DataFrame({'country': df['country']})
	fd['count'] = fd.groupby('country')['country'].transform('size')
	fd = fd.sort_values('count', ascending=False)
	fd.drop_duplicates('country', keep='first', inplace=True)
	fd.to_csv('data/countries.csv')

def main(js):
	kickDF = pd.read_json('data/'+js)
	userCmpns(kickDF)
	top = userSuccess(kickDF)
	#freedoms(top, kickDF)
	forTableau(kickDF)


main(sys.argv[1])
#argv[1]: Kickstarter JSON data in 'data' e.g. kickCleaned.json