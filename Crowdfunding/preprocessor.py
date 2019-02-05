import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
from wordcloud import WordCloud
from collections import Counter

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import sys

def label(df):
	df['success'] = df['pledged'] / df['goal']
	df['label'] = np.where(df['success'] >= 1, 1, 0) #1: Successful, #0: Unsuccessful
	return df

def campaignLength(df):
	df['projectLength'] = df['deadline'] - df['launch']
	return df

def ids(df): #Assign currencies and countries unique IDS
	df =df.assign(countryID=(df['country']).astype('category').cat.codes)
	df =df.assign(currencyID=(df['currency']).astype('category').cat.codes)
	return df

def removeStopWords(df): #Remove stopwords in blurb and title
	stopWords = stopwords.words('english')
	#From name
	df['processedName'] = df['projectName'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stopWords)]))
	#From blurb
	df['processedBlurb'] = df['blurb'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stopWords)]))
	return df

def featureEng(df): #Add blurb len and name char count
	df['blurbLen'] = df['processedName'].apply(lambda x: len(x))
	df['nameLen'] =  df['processedBlurb'].apply(lambda y: len(y))
	return df

def removeColumns(df): #Remove unwanted columns
	df.drop(['state','projectId', 'categoryName', 'creatorName', 'success'], axis=1, inplace=True)
	df.drop(['deadline', 'launch'], axis=1, inplace=True)
	df.drop(['country','currency'], axis=1, inplace=True)
	df.drop(['projectName', 'blurb'], axis=1, inplace=True)
	return df


def main(infile ,outfile):
	kickDF = pd.read_json('data/'+infile)
	newDF = label(kickDF)
	anothaDF = campaignLength(newDF)
	yapDF = ids(anothaDF)
	newestDF = removeStopWords(yapDF)
	lastDF = featureEng(newestDF)
	finalDF = removeColumns(lastDF)

	print('Writing processed data to file...')
	finalDF.to_json('data/'+ outfile)
	print('Data written to data/'+outfile)




main(sys.argv[1], sys.argv[2])
#argv[1]:  Input Kickstarter data file
#argv[2]: Where to write processed data


