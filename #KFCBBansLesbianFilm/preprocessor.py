import numpy as np
import pandas as pd
from datetime import datetime
import time
import re
import csv
import sys
import json

from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

#Process all usernames: Assign each unique username a unique ID. Save this 'Username: ID' conversion table for use later
def convertUsernames(usernames):
	print('Creating conversion table...')

	conversionTable = {}
	users = set() #A set only contains unique values i.e if duplicate is added, origi is deleted
	ids = set()

	i = 1
	for username in set(usernames):
		users.add(username)
		ids.add(i)

		i = i+1


	conversionTable['username'] = list(users)
	conversionTable['id'] = list(ids)

	print('Conversion table of {} entries created\n'.format(len(conversionTable['username'])))
	return conversionTable


#Preprocess date: Change <Thu May 03 15:13:44  2018> to <2018-05-03 15:13:44> then convert to timestamp
def processDates(dates): #List of dates as input
	print('Processing dates...')
	processedDates = []

	for date in dates:
		sr = re.search(r'(\w{3}) (\w{3}) (\d{2}) (\d{2}):(\d{2}):(\d{2})  (\d{4})',date, re.I|re.M) #Case insentive match the string
		day = sr.group(1)
		mon = sr.group(2) 
		date = sr.group(3)
		hr = sr.group(4)
		minute = sr.group(5)
		sec = '00'
		yr = sr.group(7)

		if (mon=='Apr'):
			mn = '04'
		else:
			mn = '05'

		dt = yr+'-'+mn+'-'+date+' '+hr+':'+minute+':'+sec #The date in the format 'YYYY-MM-DD HH:MM:00'

		stamp = time.mktime(datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").timetuple())	
		processedDates.append(stamp)

	print('{} Dates Processed!\n'.format(len(processedDates)))
	return processedDates


#Preprocess text: Remove URLS, mentions, punctuations and then lowercase
def processTweets(tweets): #List of tweets as input
	print('Processing tweets...')
	puncts = '"$%&\()*+,-./:;<=>?@[\]^_`{|}~' #Punctuations
	stopWords = ['ourselves', 'hers', 'between', 'yourself', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']

	processedTweets = []
	tweetCharCount = []
	numberOfHashtags = []
	numberOfExclamations = []
	for tw in tweets:
		tw = tw.decode('utf-8').lower() #Lowercase all the things
		tw = re.sub(r'\n', "", tw) #Remove newlines
		tw = re.sub(r'(\A|\s)@(\w+)',"", tw) #Replace mentions with a space
		tw = re.sub(r'https:(.{17})', "", tw) #Replace URLS with a space
		tw = ''.join([c for c in tw if c not in puncts]) #Remove punctuations except # and !
		hashes = tw.count('#')
		exclams = tw.count('!')
		words = word_tokenize(tw)
		tw = ' '.join([d for d in words if d not in stopWords]) #Remove some stopwords
		length = len(tw)

		tweetCharCount.append(length)
		processedTweets.append(tw)
		numberOfHashtags.append(hashes)
		numberOfExclamations.append(exclams)


	print('{} Tweets Processed!!\n'.format(len(twts)))
	return processedTweets, tweetCharCount, numberOfHashtags, numberOfExclamations


#Process usernames in other files based on table created at the top
def processUsernames(usernames, table):
	print('Processing Usernames...')
	processedTweeps = []
	users = table['username']
	ids  = table['id']

	for name in usernames:
		ind = users.index(name)
		userId = ids[ind]
		processedTweeps.append(userId)

	print('Tweeps processed!\n')
	return processedTweeps

#Write processed inFile and test data to CSV files
def saveData(filename, userID, verified, followers, date, text, length, hashes, exclams, sentiment):
	print('Writing data for modelling to data/'+filename)
	with open('data/'+filename, 'a') as dmp:
		writer = csv.writer(dmp, escapechar= '\\',quoting=csv.QUOTE_MINIMAL)
		writer.writerow(['user', 'isVerified','followers', 'date', 'tweet', 'charCount', 'hashtags', 'exclamations','sentiment'])

		for i in range(len(userID)):
			writer.writerow([userID[i], verified[i], followers[i], date[i], text[i], length[i], hashes[i], exclams[i],sentiment[i]])

	print('Data successfully written.\n')


#Write conversion table too for later use
def saveConversionTable(filename, table):
	users = table['username']
	ids  = table['id']

	print('Writing conversion table to data/'+filename)
	with open('data/'+filename, 'a') as dmp:
		writer = csv.writer(dmp)
		writer.writerow(['username', 'unique ID'])

		for j in range(len(users)):
			writer.writerow([users[j], ids[j]])

	print('Conversion Table successfully written.')


def main(dump, into, out):
	#For username conversion
	corpus = pd.read_csv('data/'+dump)
	usernames = corpus['username']
	table = convertUsernames(usernames)

	#Load the data
	inFile = pd.read_csv('data/'+into)
	
	#inFile text, date and usernames for preprocessing. The rest are copied as is
	inFileText = inFile['text']
	inFileDate = inFile['date']
	inFileUsername = inFile['username']

	inFileFollowers = inFile['followers']
	inFileSentiment = inFile['sentiment']
	inFileVerified = inFile['isVerified']	

	#Processed content
	processedinFileText, inFileCharCount, inFileHashes, inFileExclams = processTweets(inFileText)
	processedinFileDate = processDates(inFileDate)
	processedinFileUsername = processUsernames(inFileUsername, table)

	#Save to processed data to usable CSV files
	saveData(out, processedinFileUsername, inFileVerified, inFileFollowers, processedinFileDate, processedinFileText, inFileCharCount, inFileHashes, inFileExclams, inFileSentiment)

	
	#Save conversion table
	saveConversionTable('conversionTable.csv', table)


main(sys.argv[1], sys.argv[2], sys.argv[3])
