import pandas as pd
import json
import sys

def main(inputFile, outputFile):
	print('JSON creation begins...')
	dump = pd.read_csv('data/'+inputFile)

	ids = dump['project_id'].tolist()
	names = dump['title'].tolist()
	blurbs = dump['tagline'].tolist()
	pesa = dump['currency'].tolist()
	category = dump['category'].tolist()
	deadlines = dump['close_date'].tolist()
	launches = dump['open_date'].tolist()
	percents = dump['funds_raised_percent'].tolist()

	obj = {}
	obj['projects'] = []

	for j in range(len(ids)):
		item = {}
		item['projectId'] = ids[j]
		item['projectName'] = names[j]
		item['blurb'] = blurbs[j]
		item['currency'] = pesa[j]
		item['categoryName'] = category[j]
		item['deadline'] = deadlines[j]
		item['launch'] = launches[j]
		item['percentageRaised'] = percents[j]

		obj['projects'].append(item)

	with open('data/'+outputFile, 'a') as dp:
		json.dump(obj, dp)

	print('JSON creation done... {} items written'.format(len(obj['projects'])))


main(sys.argv[1], sys.argv[2])
#argv[1]: Input CSV (downloaded from goo.gl/6pCJb) e.g. indie.csv
#argv[2]: The JSON to dump into e.g. out.json
#All read from and written into data/ 