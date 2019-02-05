import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
from wordcloud import WordCloud
from collections import Counter


from datetime import datetime
import time
import re

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

sns.set(style="whitegrid")
sns.set_style('ticks')
#Indiegogo: Index([u'blurb', u'categoryName', u'currency', u'deadline', u'launch',
#       u'percentageRaised', u'projectId', u'projectName'],
#      dtype='object')
#Kickstarter: Index([u'backers', u'blurb', u'categoryId', u'categoryName', u'country',
#       u'creatorId', u'creatorName', u'currency', u'deadline', u'goal',
#       u'launch', u'pledged', u'projectId', u'projectName', u'state'],
#      dtype='object')


def featureExtractor(df, feature, category=None, dates=None, dateRange=None): 
	g = df[feature].tolist()
	if(category is not None): #Return dict of category vs list of feature
		dicto = {}
		f = df['categoryName'].tolist()
		for item in category:
			dicto[item] = []
			arr = [i for i,vals in enumerate(f) if vals==item] #Get indices of rows 
			for j in range(len(arr)):
				k = arr[j]
				dicto[item].append(g[k])

		keys=[]
		for key, value in dicto.iteritems():
			keys.append(key)
		return dicto, keys

	elif(dates is not None): #Extract for a date range
		attrs = []
		arr = [i for i, vals in enumerate(dates) if vals>=dateRange]
		for j in range (len(arr)):
			k = arr[j]
			attrs.append(g[k])
		return attrs

	elif(category is None): #Extract all
		ls = df[feature].tolist()
		return ls

def toTimeStamp(dates): #Convert all dates to timestamps
	processedDates = []
	for date in dates:
		if(date != 'null'):
			sr = re.search(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})', date, re.I|re.M)
			yr = sr.group(1)
			mn = sr.group(2) 
			date = sr.group(3)
			hr = sr.group(4)
			minute = sr.group(5)
			sec = sr.group(6)

			dt = yr+'-'+mn+'-'+date+' '+hr+':'+minute+':'+sec #The date in the format 'YYYY-MM-DD HH:MM:00'

			stamp = time.mktime(datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").timetuple())	
			processedDates.append(stamp)
	return processedDates
	


def popular(dic, allDic): #Extract top 5 
	put = {}
	put['item']=[]
	put['count'] = []

	for j in range(3):
		item = dic[j]
		count = allDic[item]
		put['item'].append(item)
		put['count'].append(count)

	return put

def processWords(dic, shafi): #Return blurbs and titles without stopwords
	stopWords = stopwords.words('english')
	processed ={}
	lns = []
	for j in range(len(shafi)):
		key = shafi[j]
		corp = dic[key]
		processed[key] = []
		for sent in corp:
			if(type(sent) is not float):
				sent = sent.encode('ascii','ignore').decode('ascii')
			else:
				sent = ''
			words = word_tokenize(sent)
			tw = ' '.join([d for d in words if d not in stopWords]) #Remove stopwords
			processed[key].append(tw)
	return processed

def makeCloud(dic, shafi, cloudType, platform): #Corpus is a string of all words
	for i in range(len(shafi)):
		key = shafi[i]
		ls = dic[key]
		maj = []
		for it in ls:
			wds = it.split(' ')
			for j in range(len(wds)):
				maj.append(wds[j])
		corpus = ' '.join([f for f in maj])
		cloud = WordCloud(max_font_size=40, background_color=None, mode='RGBA', colormap='inferno').generate(corpus)
		plt.figure()
		plt.imshow(cloud, interpolation="bilinear")
		plt.axis("off")
		plt.title('Category Rank '+str(i+1)+' on '+platform+' '+key+' '+cloudType+' Word Cloud')
		plt.show()


def categoryPopularity(ind, kck):
	#Categories for all campaigns
	allIndCat = featureExtractor(ind, 'categoryName')
	allKickCat = featureExtractor(kck, 'categoryName')

	#Check count (Returns a dict of category name vs count, sorted by count desc)
	countedInd = dict(Counter(allIndCat))
	countedKick = dict(Counter(allKickCat))
		#Return list of dict keys sorted in count DESC
	sortedInd = sorted(countedInd, key=countedInd.get, reverse=True) 
	sortedKick = sorted(countedKick, key=countedKick.get, reverse=True)

	#Get top 5 categories for each 
	topInd = popular(sortedInd, countedInd)
	topKick = popular(sortedKick, countedKick)

	#Plot bar charts
	sns.barplot(topInd['count'], topInd['item'])
	plt.title('INDIEGOGO TOP CATEGORIES')
	plt.show()
	sns.despine()

	sns.barplot(topKick['count'], topKick['item'])
	plt.title('KICKSTARTER TOP CATEGORIES')
	plt.show()
	sns.despine()

	return topInd, topKick
	

def titleCloud(ind, kck, indCmpns, kckCmpns):
	#Titles for top 5 campaigns
	allIndTit, shafiInd = featureExtractor(ind, 'projectName', indCmpns)
	processedInd = processWords(allIndTit, shafiInd)
	makeCloud(processedInd, shafiInd, 'Name', 'Indiegogo')

	allKckTit, shafiKck = featureExtractor(kck, 'projectName', kckCmpns)
	processedKck = processWords(allKckTit, shafiKck)
	makeCloud(processedKck, shafiKck, 'Name', 'Kickstarter')		


def success(ind, kck, indCmpns, kckCmpns):
	indieLaunch = toTimeStamp(ind['launch'])
	kckLaunch = kck['launch'].tolist()

	indieSucc = featureExtractor(ind, 'percentageRaised', None, indieLaunch, 1496324901)
	kckGoal = np.array(featureExtractor(kck, 'goal', None, kckLaunch, 1496324901))
	kckPled = np.array(featureExtractor(kck, 'pledged', None, kckLaunch, 1496324901))
	kckSucc = (kckPled/kckGoal)

	indieIs = [i for i,vals in enumerate(indieSucc) if vals>='1' and vals != 'null' and vals.find('E')<0] #Successful Indiegogo Projects
	kckIs = [j for j,vals in enumerate(kckSucc) if vals>=1]

	#Get successeful and unsuccessful
	successfulIndie = len(indieIs)
	unsuccessfulIndie = len(indieSucc) - successfulIndie

	successfulKck = len(kckIs)
	unsuccessfulKck = kckSucc.shape[0] - successfulKck


	#Grouped bar plot!!!
	data = pd.DataFrame([['Indiegogo', 'Successful', successfulIndie], ['Indiegogo', 'Failed', unsuccessfulIndie], ['Kickstarter', 'Successful', successfulKck], ['Kickstarter', 'Failed', unsuccessfulKck]], columns=['Platform','State', 'Value'])
	data.pivot('Platform', 'State', 'Value').plot(kind='bar')
	plt.xlabel('Platform', fontsize=15)
	plt.ylabel('Campaigns', fontsize=15)
	plt.xticks(fontsize=10, rotation=10)
	plt.title('Successful vs Failed Campaigns', fontsize=20)
	sns.set()
	plt.show()

	return indieIs, kckIs

def successfulCategories(ind, kck, succIndie, succKck):
	indCategs = featureExtractor(ind, 'categoryName')
	kckCategs = featureExtractor(kck, 'categoryName')

	succIndCats=[]
	succKckCats = []

	for i in range(len(succIndie)):
		succIndCats.append(indCategs[succIndie[i]])

	for j in range(len(succKck)):
		succKckCats.append(kckCategs[succKck[j]])

	#Check count (Returns a dict of category name vs count, sorted by count desc)
	countedInd = dict(Counter(succIndCats))
	countedKick = dict(Counter(succKckCats))
		#Return list of dict keys sorted in count DESC
	sortedInd = sorted(countedInd, key=countedInd.get, reverse=True) 
	sortedKick = sorted(countedKick, key=countedKick.get, reverse=True)

	#Get top 5 categories for each 
	topInd = popular(sortedInd, countedInd)
	topKick = popular(sortedKick, countedKick)

	#Plot bar charts
	sns.barplot(topInd['count'], topInd['item'])
	plt.title('INDIEGOGO MOST SUCCESSFUL CATEGORIES')
	plt.show()
	sns.despine()

	sns.barplot(topKick['count'], topKick['item'])
	plt.title('KICKSTARTER MOST SUCCESSFUL CATEGORIES')
	plt.show()
	sns.despine()

	return topInd, topKick


def main(kickjs, indiejs):
	kickDF = pd.read_json('data/'+kickjs)
	with open('data/'+indiejs, 'r') as dm:
		dat = json.load(dm)
	indieDF = pd.DataFrame(dat['projects'])

	topIndieCat, topKickCat = categoryPopularity(indieDF, kickDF) #Plot top 3 most populated categories for each
	succIndie, succKck = success(indieDF, kickDF, topIndieCat['item'], topKickCat['item']) #Plot 'successful vs failed'
	topInd, topKck = successfulCategories(indieDF, kickDF, succIndie, succKck) #Plot successful categories
	titleCloud(indieDF, kickDF, topInd['item'], topKck['item']) #Wordclouds for names in successful categories
	
main(sys.argv[1], sys.argv[2])
#argv[1]: Kickstarter JSON
#argv[2]: Indie JSON