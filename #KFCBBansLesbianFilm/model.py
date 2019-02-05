import sys
import timeit
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix  

from sklearn.ensemble import RandomForestClassifier


#user,isVerified,followers,date,tweet,vectors,charCount,hashtags,exclamations,sentiment

def genDataFrame(df):
	usernames = df['user'].tolist()
	verified = df['isVerified'].tolist()
	noOfFollowers = df['followers'].tolist()
	tweetedDate = df['date'].tolist()
	tweetText = df['tweet'].tolist()
	tweetLength = df['charCount'].tolist()
	noOfHashtags = df['hashtags'].tolist()
	noOfExclams = df['exclamations'].tolist()

	

	#Vectorise the tweets using SKLearn TFIDF
	vectorizertr = TfidfVectorizer(ngram_range = ( 1, 3), analyzer="word" , binary=False, sublinear_tf=False, max_features=300)

	#When the corpus is too large, TfIdf returns lists containing '...' Therefore, vectorise in batches
	k = 0
	j = 10
	ln = len(tweetText)
	twits = []
	while k<ln:
		corpus = []
		corpus = tweetText[k:j]
		vec = []
		vec = vectorizertr.fit_transform(corpus).toarray()
		
		for g in range(len(vec)):
			v = vec[g]
			if(v.shape[0]<300):
				y = 300 - (v.shape[0])
				f = np.pad(v, (y, 0), 'minimum')
				f = f.reshape(300,)
				f = f.sum()
				twits.append(f)

			else:
				v = vec[g]
				v = v.sum()
				twits.append(v)

			

		
		k = k+10
		j = j+10
	
	twits = np.array(twits)	
	
	newDf = pd.DataFrame({'users':usernames, 'ver':verified, 'foll':noOfFollowers, 'date':tweetedDate, 'ln':tweetLength, 'hash':noOfHashtags, 'exc':noOfExclams, 'vec':twits})

	return newDf


def runModel(xTrain, yTrain, xTest, yTest, xUnlabeled, yUnlabeled):
	start = timeit.default_timer()
	#INTIALISE A RANDOM FOREST CLASSIFIER
	rfc = RandomForestClassifier()

	#INITIALISE SOME PARAMS TO BE TESTED
	rfcParameterGrid = {'n_estimators':[5,10,25,50],
						'criterion':['gini','entropy'],
						'max_features':[1,2,3,4,5,6,7,8],
						'warm_start':[True, False],
						'class_weight':['balanced', 'balanced_subsample', {0: 1, 1: 10}, {0: 1, 1: 3}, {0: 1, 1: 5}, {0: 1, 1: 1}] #The dicts are weight for our classes i.e. 0-10, 1-3, 2-5, 3-1
						}

	#USE K-FOLD CROSS-VALIDATION
	folds = StratifiedKFold(n_splits=10)

	#FIND THE BEST PARAMETERS FOR THE MODEL
	rfcgrid_search = GridSearchCV(rfc, param_grid = rfcParameterGrid, cv=folds)

	#FIT THE MODEL TO THE DATA
	rfcgrid_search.fit(xTrain, yTrain)

	#CHOOSE THE BEST CLASSIFIER
	rfc = rfcgrid_search.best_estimator_
	print(rfcgrid_search.best_params_) #Print the best hyperparams

	#TEST ACCURACY USING THE DATA
	print('Accuracy for 10 folds: {}'.format(cross_val_score(rfc, xTrain, yTrain, cv=10)))

	y_pred = rfc.predict(xTest)
	print('Confusion Matrix:\n {}'.format(confusion_matrix(yTest, y_pred)))
	print('Report:\n {}'.format(classification_report(yTest, y_pred)))

	values = rfc.feature_importances_
	attrs = xTrain.columns
	for i in range(len(values)):
		print('Attr: {}.          Importance: {}'.format(attrs[i], values[i]))

	print('Time elapsed to fit and test: {}'.format(timeit.default_timer() - start))


	#Run on unseen data
	yUnlabeled = rfc.predict(xUnlabeled)
	xUnlabeled['sentiment'] = yUnlabeled

	xUnlabeled[['users', 'sentiment']].to_csv('data/preds.csv')


def main (trainFile, testFile, unlabeledFile):
	train = pd.read_csv('data/'+trainFile)
	test = pd.read_csv('data/'+testFile)
	unlabeled = pd.read_csv('data/'+unlabeledFile)


	trainX = genDataFrame(train) 
	testX = genDataFrame(test)
	unlabeledX = genDataFrame(unlabeled)

	trainY = train['sentiment']
	testY = test['sentiment']
	unlabeledY = []

	runModel(trainX, trainY, testX, testY, unlabeledX, unlabeledY)


main(sys.argv[1], sys.argv[2], sys.argv[3])
