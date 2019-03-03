# Clean up the downloaded character data as per https://www.kaggle.com/mylesoneill/game-of-thrones -- character_predictions
import ast
import pandas as pd
import json

csvFile = '../../data/raw/character_features.csv' 

df = pd.read_csv(csvFile)


df.drop(['S.No', 'actual', 'pred', 'alive', 'plod', 'DateoFdeath', 'boolDeadRelations', 'isPopular', 'popularity', 'isAlive'], axis = 1, inplace = True)
df.rename(columns = {'dateOfBirth': 'date_of_birth', 'isAliveMother': 'mother_is_alive', 'isAliveFather': 'father_is_alive', 'isAliveHeir': 'heir_is_alive', 'isAliveSpouse': 'spouse_is_alive', 'isMarried': 'married', 'isNoble': 'nobility', 'numDeadRelations':'number_of_dead_relations'}, inplace = True)

df1 = df

# Update manually: mother, father and spouse
fillGaps = '../../data/raw/filling_gaps.txt' # Lines with JSONs to add to/ correct df
with open(fillGaps, 'r') as fill:
	additions = fill.readlines()

additions = [x.strip() for x in additions] 
additions = [ast.literal_eval(y) for y in additions] # Convert to dict


for add in additions:
	for k,v in add.iteritems():
		if(k != 'name'):
			df1.loc[df1['name'] == add['name'], k] = v


charactersCSV = '../../data/interim/character_features.csv' 
df1.to_csv(charactersCSV, index = False)
