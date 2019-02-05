import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from wordcloud import WordCloud

def returnFeatures(df):
	usernames = df['user'].tolist()
	verified = df['isVerified'].tolist()
	noOfFollowers = df['followers'].tolist()
	tweetedDate = df['date'].tolist()
	tweetText = df['tweet'].tolist()
	tweetVector = df['vectors'].tolist()
	tweetLength = df['charCount'].tolist()
	noOfHashtags = df['hashtags'].tolist()
	noOfExclams = df['exclamations'].tolist()
	senti = df['sentiment'].tolist()
	
	return usernames, verified, noOfFollowers, tweetedDate, tweetText, tweetVector, tweetLength, noOfHashtags, noOfExclams, senti


def getPerSentiment(feature, labels, senti):
	arr = [i for i,vals in enumerate(labels) if vals==senti] #Get indices of rows of the sentiment

	values = []
	for j in range(len(arr)):
		k = arr[j]
		values.append(feature[k])

	vals = np.array(values)

	if((vals.dtype) == 'int64'): #Is it a numeric array
		avg = np.mean(vals)
		return avg
	else:
		words = []
		for i in range(len(vals)):
			sent = vals[i].split(' ')
			for j in range(len(sent)):
				words.append(sent[j])
		
		maj = [k for k in words if k!='kfcbbanslesbianfilm']
		wds = ' '.join([i for i in maj])
		return wds
	

def plotBar(labels, y, title, labelX, labelY):
    x = np.arange(len(y))
    graph = plt.bar(x, y)
    graph[0].set_color('#ff0000')
    graph[1].set_color('#00FFFF')
    graph[2].set_color('#008000')
    graph[3].set_color('#000000')

    plt.xlabel(labelX, fontsize=15)
    plt.ylabel(labelY, fontsize=15)
    plt.xticks(x, labels, fontsize=10, rotation=0)
    plt.title(title, fontsize=20)
    plt.show()

def plotCloud(corpus):
	cloud = WordCloud(max_font_size=40).generate(corpus)
	plt.figure()
	plt.imshow(cloud, interpolation="bilinear")
	plt.axis("off")
	plt.show()

#def plotPieChart(x, lbls):
#	explode = (0.05,0.05,0.05, 0.05)
#	cls = ['#ff0000','#00FFFF','#008000','#000000']
#	plt.pie(x, labels=lbls, colors=cls, autopct='%1.1f%%', explode=explode)
#	plt.show()

def generatePlots(hashtags, exclamations, length,text, labels):
	#Average number of hashtags vs sentiment
	phobicAvg = getPerSentiment(hashtags, labels, 0)
	neutralAvg = getPerSentiment(hashtags, labels, 1)
	philicAvg = getPerSentiment(hashtags, labels, 2)
	garbageAvg = getPerSentiment(hashtags, labels, 3)

	hashesAvg = [phobicAvg, neutralAvg, philicAvg, garbageAvg]
	lbls = ['Homophobic', 'Neutral', 'Homophilic', 'Garbage']
	title ='NUMBER OF HASHTAGS VS SENTIMENT'
	xlbl = 'Sentiment'
	ylbl = 'Hashtags (Average)'

	plotBar(lbls, hashesAvg, title, xlbl, ylbl)

	#Average number of exclamation points vs sentiment
	phobicEAvg  = getPerSentiment(exclamations, labels, 0)
	neutralEAvg  = getPerSentiment(exclamations, labels, 1)
	philicEAvg  = getPerSentiment(exclamations, labels, 2)
	garbageEAvg = getPerSentiment(exclamations, labels, 3)

	exclamAvgE = [phobicEAvg, neutralEAvg, philicEAvg, garbageEAvg]
	titleE ='NUMBER OF EXCLAMATION POINTS VS SENTIMENT'
	xlblE = 'Sentiment'
	ylblE = 'Exclamations (Average)'

	plotBar(lbls, exclamAvgE, titleE, xlblE, ylblE)

	#Average tweet length vs sentiment
	phobicLAvg= getPerSentiment(length, labels, 0)
	neutralLAvg= getPerSentiment(length, labels, 1)
	philicLAvg= getPerSentiment(length, labels, 2)
	garbageLAvg= getPerSentiment(length, labels, 3)

	lnAvg = [phobicLAvg, neutralLAvg, philicLAvg, garbageLAvg]
	titleL ='TWEET LENGTH VS SENTIMENT'
	xlblL = 'Sentiment'
	ylblL = 'Tweet Length (Average)'

	plotBar(lbls, lnAvg, titleL, xlblL, ylblL)

	#Word cloud vs sentiment
	phobicW = getPerSentiment(text, labels, 0)
	neutralW = getPerSentiment(text, labels, 1)
	philicW = getPerSentiment(text, labels, 2)
	garbageW = getPerSentiment(text, labels, 3)

	plotCloud(phobicW)
	plotCloud(neutralW)
	plotCloud(philicW)
	plotCloud(garbageW)



def main(csvFile):
	print('Reading data...')
	train = pd.read_csv('data/'+csvFile)
	print('Data read successful')

	print('Starting visualisation...')
	#Extract features
	Trainusernames, Trainverified, TrainnoOfFollowers, TraintweetedDate, TraintweetText, TraintweetVector, TraintweetLength, TrainnoOfHashtags, TrainnoOfExclams, Trainsenti = returnFeatures(train)
	
	#Plot some plots
	generatePlots(TrainnoOfHashtags, TrainnoOfExclams, TraintweetLength, TraintweetText, Trainsenti)
	print('Visualisation complete.')


main(sys.argv[1])

