import sys
import timeit
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix 

from xgboost import XGBClassifier
from xgboost import plot_importance

import sys

#[u'backers', u'blurbLen', u'categoryId', u'countryID', u'creatorId',
       #u'currencyID', u'goal', u'label', u'nameLen', u'pledged',
       #u'processedBlurb', u'processedName', u'projectLength']
def vectoriser(df): #Vectorise blurb and name
	vec = TfidfVectorizer(ngram_range=(1,1), analyzer='word', max_df=1.0, binary=False, sublinear_tf=False)

	corpus = df['processedName']
	corp = df['processedBlurb']
	df['nameToVec'] = list(vec.fit_transform(corpus).toarray())
	df['projectName'] = df['nameToVec'].apply(lambda x: x.sum())

	df['blurbToVec'] = list(vec.fit_transform(corp).toarray())
	df['blurb'] = df['blurbToVec'].apply(lambda y: y.sum())

	df.drop(['processedName', 'processedBlurb', 'nameToVec', 'blurbToVec'], axis=1, inplace=True)
	return df


def classify(dfTrain, dfTest, outFile):
	dfTrain.drop(['pledged', 'goal', 'backers'], axis=1, inplace=True) #Exclude the obvious markers of success
	dfTest.drop(['pledged', 'goal', 'backers'], axis=1, inplace=True)

	x = dfTrain[dfTrain.columns[dfTrain.columns != 'label']]
	y = dfTrain['label']

	XTrain, XTest, yTrain, yTest = train_test_split(x, y, test_size=0.33, random_state=42)

	sgd = XGBClassifier()
	sgd.fit(XTrain, yTrain)

	#TEST ACCURACY USING THE DATA
	print('Accuracy for 10 folds: {}'.format(cross_val_score(sgd, XTrain, yTrain, cv=10)))

	y_pred = sgd.predict(XTest)
	print('Confusion Matrix:\n {}'.format(confusion_matrix(yTest, y_pred)))
	print('Report:\n {}'.format(classification_report(yTest, y_pred)))

	plot_importance(sgd)
	plt.show()

	#Label unseen data
	preds = sgd.predict(dfTest)
	dfTest['label'] = preds
	dfTest.to_json('data/'+outFile)


def main(labeledFile, unlabeledFile, theLabels):
	start = timeit.default_timer()

	dfTr = pd.read_json('data/'+labeledFile)
	dfTe = pd.read_json('data/'+unlabeledFile)
	fdTr = vectoriser(dfTr)
	fdTe = vectoriser(dfTe)
	classify(fdTr, fdTe, theLabels)

	print('Time elapsed to fit, test and label: {}'.format(timeit.default_timer() - start))


main(sys.argv[1], sys.argv[2], sys.argv[3])
#argv[1]: Labeled processed file
#argv[2]: Unlabeled processed file
#argv[3]: The labeled file

'''
Accuracy for 10 folds: [ 0.7755102 0.77868852  0.77459016  0.76229508  0.7704918 0.76131687 0.781893  0.7654321 0.77366255  0.77777778]
Confusion Matrix:
 [[909  15]
 [256  21]]
Report:
              				precision    recall  f1-score   support

          Unseccessful       0.78      0.98      0.87       924
          Successful         0.58      0.08      0.13       277

		avg / total          0.73      0.77      0.70      1201

------------ PREDICTIONS ------------------

CREATOR ID 		Non-obv  Obv			PROJECT NAME

1393117251      0 		0				Gafas de Sol Ecol\u00f3gicas | Carpris Sunglasses
169431282   	0 		0				Project for soyamax join to JAPAN EXPO 2019 in Paris
1913919714  	0 		1 				The Witch's Cupboard: Potions & Ingredients Hard Enamel Pins
746960005  		0 		0				Ultra Entertainment : A Business
1953914200 		0 		0				Karama Yemen Human Rights Film Festival
1112471646 		0 		0				The Witches Compendium: A guide to all things Wicca
1897792658      0  		0				Quickstarter: CELIE & COUCH
1896424317 		0 		0				Tiger Friday
319069410 		0 		0				Vainas De Vainilla - Vanilla Bean
1185361668 		0 		0				\"Simone de Beauvoir\" Libro Ilustrado/Picture Book
1654923401 		0 		0				Artist Lost/Heiress Denied - A True Story
1085361967 		0 		0				Stolen Weekend's debut EP
1614906331 		0 		0				Maidens of the dragon, 28mm quality pewter miniatures.
2144042739 		0 		0				Little Tumble Romp Indoor Sensory Center
669534979  		0 		0				Watercolour Style - Nebula Washi Stickers
1645694895 		0 		0				HOWPACKED.COM New nightlife monitoring website version 1	
766857030 		0 		0				Boob Planter Pins
1399345714 		0 		0				Operation: Boom - Issue 3
441879431  		0 		0				Rapture VR
341062337  		0 		0				Goos'd - Bring the party and Get Goos'd!
1157356534 		1 		0				Smuggles n' Snuggles
1354754923 		0 		0				Makeshift
1124463580 		0 		0				Creative Community Project
1224124211 		0 		0				Opening a fabric store in Downtown Kent!

'''