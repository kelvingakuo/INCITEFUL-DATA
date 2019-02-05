import pandas as pd
import numpy as np
import math
import seaborn as sns
import matplotlib.pyplot as plt
from pywaffle import Waffle
import cv2
from PIL import Image
from scipy.misc import imread
from nltk.corpus import stopwords
from sklearn.feature_extraction import text 
from wordcloud import WordCloud
from afinn import Afinn

from collections import Counter
import sys
import csv

sns.set(style='whitegrid')
def cleanDataset(df):
	stopWords = text.ENGLISH_STOP_WORDS.union(["I", "like", "I'm", "don't", "ain't", "got", "know", "You", "And", "But", "can't", "just"])
	#Check for, and remove empty lyrics
	df['lyric'].replace('',np.nan,inplace=True)
	df.dropna(subset=['lyric'], inplace=True )

	#Remove '\n' from lyric and song name and stopwords
	#From lyric
	df['noComma'] = df['lyric'].apply(lambda x: x.replace(',',' '))
	df['lastLyric'] = df['noComma'].apply(lambda x: ' '.join([word for word in x.split() if word not in stopWords]))
	#From name
	df['cleanName'] = df['name'].apply(lambda x: x.replace('\n',''))
	df['lastName'] = df['cleanName'].apply(lambda x: x.replace('Lyrics', ''))
	#From artist
	df['lastArtist'] = df['artist'].apply(lambda x: x.replace('Lyrics', ''))
	df.drop(['lyric','name', 'cleanName', 'noComma', 'artist'], axis=1, inplace=True)
	df.rename(columns={'lastLyric':'lyric', 'lastName':'name', 'lastArtist':'artist'}, inplace=True)
	return df

def genStackedPlotData(df):
	#Group artist by year and get count
	print("Generating data for Tableau...")
	df.drop(['lyric','name','link'], axis=1, inplace=True)
	fd = df.groupby(['year','artist']).agg(np.size).reset_index(name='count')
	fd.to_csv('data/forChart.csv')
	print("Data for Tableau generated.")


def lenComp(df):
	df['lyricLength'] = df['lyric'].apply(lambda y: len(y.split()))
	df.drop(['year','name','link', 'lyric'], axis=1, inplace=True)
	fd = df.groupby(['artist']).agg(np.median).reset_index()
	
	sf = fd.sort_values('lyricLength', ascending=False)
	g = sns.barplot(x=sf['artist'], y=sf['lyricLength'], data=sf)
	g.set_xticklabels(sf['artist'], rotation=15)
	plt.title("ARTIST SONG LENGTH")
	plt.ylabel("SONG LENGTH (MEDIAN)")
	plt.xlabel("ARTIST")
	plt.show()

def drawMap(nm): #Create a map for wordclouding from name
	ln = len(nm)
	img = np.zeros((612, ln*420, 3), np.uint8)

	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(img,nm,(0,500), font, 18, (255,255,255),85)
	img = 255-img
	cv2.imwrite('name.jpg', img)
	return img


def drawCloud(name, corpus, title, isCorp=False):
	drawMap(name)
	img = Image.open("name.jpg")
	hcmask = np.array(img)

	if(isCorp):
		wordcloud = WordCloud(mask=hcmask, min_font_size=10, background_color=None, mode='RGBA', colormap='gist_rainbow').generate(corpus)
	else:	
		wordcloud = WordCloud(mask=hcmask, min_font_size=10, background_color=None, mode='RGBA', colormap='gist_rainbow').generate_from_frequencies(corpus)

	plt.title(title, size=30, y=1.01)
	plt.imshow(wordcloud, interpolation="bilinear")
	plt.axis("off")
	plt.figure()
	plt.show()

def returnCorpus(df, artist=None, ls=None):
	if(ls is not None):
		lyrs = dict()
		lyrs['artist'] = []
		lyrs['corp'] = []

		for ar in ls:
			ind = np.where(df['artist']==ar)[0]
			corp = ' '.join(df.iloc[ind, :]['lyric'].tolist()).encode('utf-8')
			lyrs['artist'].append(ar)
			lyrs['corp'].append(corp)
		return lyrs
		
	elif(ls is None):
		indj = np.where(df['artist']==artist)[0]
		corpus = ' '.join(df.iloc[indj, :]['lyric'].tolist()).encode('utf-8')
		return corpus



def wordsUsed(df):
	df.drop(['year','name','link'], axis=1, inplace=True)
	jayCorp = returnCorpus(df, u'Jay-Z ')
	nasCorp = returnCorpus(df, u'Nas ')
	nickiCorp = returnCorpus(df, u'Nicki Minaj ')
	cardiCorp = returnCorpus(df, u'Cardi B ')
	draCorp = returnCorpus(df, u'Drake ')
	wayneCorp = returnCorpus(df, u'Lil Wayne ')

	drawCloud("Jay-Z", jayCorp, "Jay-Z")
	drawCloud("Nas", nasCorp, "Nas")
	drawCloud("Drake", draCorp, "Drake ")
	drawCloud("Weezy", wayneCorp, "Lil Wayne")
	drawCloud("Nicki", nickiCorp, "Nicki Minaj")
	drawCloud("Cardi", cardiCorp, "Cardi B")

	#Jay Z vs Nas <The beef>
	#Drake vs Weezy <YMCMB>
	#Cardi vs Nicki <The ladies>

def totalFreq(df):
	corpus = ' '.join(df['lyric'].tolist()).encode('utf-8')

	arr = corpus.split()
	counter = Counter(arr)
	top = dict(counter.most_common(500))

	drawCloud("HIP-HOP", top, "THIS IS HIP-HOP", False)


def frequentWords(df):
	cels = df.artist.unique()
	corpDict = returnCorpus(df, None, cels)

	i = 0
	while (i<len(corpDict['artist'])):
		arr = corpDict['corp'][i].split()
		counter = Counter(arr)
		top = dict(counter.most_common(100))

		tt = corpDict['artist'][i]
		mp = corpDict['artist'][i].split(' ',1)[0]
		drawCloud(mp, top, tt, False)

		i=i+1 

def senti(df): #AFINN to check -ve vs +ve 
	afinn = Afinn()

	cels = df.artist.unique()
	corpDict = returnCorpus(df, None, cels)

	sent = dict()
	sent['artist'] = []
	sent['score'] = []
	j = 0
	while(j<len(corpDict['artist'])):
		sc = afinn.score(corpDict['corp'][j])
		art = corpDict['artist'][j]
		sent['artist'].append(art)
		sent['score'].append(sc)
		j=j+1

	fd = pd.DataFrame.from_dict(sent)
	fd.sort_values('score', ascending=False, inplace=True)
	g = sns.barplot(x=fd['artist'], y=fd['score'], data=df)
	g.set_xticklabels(fd['artist'], rotation=15)
	plt.title("ARTIST MUSIC SENTIMENT")
	plt.ylabel("SENTIMENT")
	plt.xlabel("ARTIST")
	plt.show()

	

def hesabu(needle, haystack):
	count = dict(Counter(haystack.split()).most_common())
	items = dict()
	total = 0
	for key in count.keys():
		if(key in needle):
			items[key] = count.get(key)
			total = total + count.get(key)
	return items, total

def occurences(df):
	drugs = ['weed', 'blunt', 'pot', 'chronic', 'ganja', 'cannabis', 'henny', 'hennessy', 'cristal', 'patron', 'bacardi', 'moet', 'molly', 'crack', 'cocaine', 'ganja', 'mdma', 'ecstasy', 'purple', 'coke']
	sex = ['pussy', 'hoes', 'bitches', 'bitch', 'booty', 'balls deep', 'sex', 'ass', 'bone', 'DTF', 'fucking']
	money = ['money', 'dough', 'bands', 'benjamins', 'cheddar', 'buck', 'bucks', 'dinero', 'pesos', 'quid']

	#Calc item occurence
	df['lyricLength'] = df['lyric'].apply(lambda y: len(y.split()))

	df['drugs'] = df['lyric'].apply(lambda x: hesabu(drugs, x))
	df['sex'] = df['lyric'].apply(lambda x: hesabu(sex, x))
	df['money'] = df['lyric'].apply(lambda x: hesabu(money, x))


	#Get totals and percentages
	df['drugsTotal'] = df['drugs'].apply(lambda x: x[1])
	df['sexTotal'] = df['sex'].apply(lambda x: x[1])
	df['moneyTotal'] = df['money'].apply(lambda x: x[1])
	df['total'] = df['drugsTotal'] + df['sexTotal'] + df['moneyTotal']
	df['percentage'] = (df['total'] / df['lyricLength']) * 100

	df.drop(['year','link', 'lyric'], axis=1, inplace=True)

	return df


def finalPlots(df):
	#Waffle chart of lyric distribution
	medianLen = math.ceil(np.average(df['lyricLength']))
	drugs = math.ceil(np.average(df['drugsTotal']))
	sex = math.ceil(np.average(df['sexTotal']))
	money = math.ceil(np.average(df['moneyTotal']))
	rest= medianLen - (drugs+sex+money)

	data = {'Drugs' : drugs,'Sex' : sex, 'Money': money, 'Others' :rest}
	
	
	fig = plt.figure(
		FigureClass=Waffle, 
		rows=4, 
		columns=71,
		values = data, 
		colors = ('#ff0000', '#0000cc', '#006600', '#000000'),
		legend = {'loc': 'lower left', 'bbox_to_anchor': (0, -0.4), 'ncol': len(data), 'framealpha': 0}
		)
	plt.title('A BREAKDOWN OF LYRICAL CONTENT FOR A SONG')
	plt.show()

	#Worst offenders
	df = df[['artist','percentage']]
	fd = df.groupby(['artist']).agg(np.mean).reset_index()
	sf = fd.sort_values('percentage', ascending=False)
	g = sns.barplot(x=sf['artist'], y=sf['percentage'], data=sf)
	g.set_xticklabels(sf['artist'], rotation=15)
	plt.title("ARTIST VS OCCURENCE OF DRUGS, SEX AND MONEY")
	plt.ylabel("DRUGS, SEX, MONEY (% of song)")
	plt.xlabel("ARTIST")
	plt.show()

	
	


def main(fil):
	lrs = pd.read_json('data/'+fil)
	clean = cleanDataset(lrs)

	genStackedPlotData(lrs)
	lenComp(clean)
	wordsUsed(clean)
	totalFreq(clean)
	frequentWords(clean)
	senti(clean)
	cts = occurences(clean)
	finalPlots(cts)
	


main(sys.argv[1])
#argv[1]: Lyrics JSON data in 'data' e.g. lyrics.json