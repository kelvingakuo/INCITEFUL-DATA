* Each file can be run from the terminal without needing to change the code.
* All input and output files are assumed to be located inside and will be written into 'data/'
* When running each file, the command is of the following format 'python code.py aFileHere anotherFileHere anExtraFile'
	- Henceforth, the first file after code.py is argv[1], the second argv[2] and so forth


1. wrangler.py
-> Bot to collect ALL the tweets of a hashtag provided they have been tweeted within the past week
#argv[1]: Hashtag without the '#' e.g. Arsene when searching for #Arsene
#argv[2]: The JSON file to store the tweet objects returned e.g. data.json 

2. parser.py
-> Code to return a human readable CSV file containing the chosen attributes, extracted from the file returned by wrangler.py
#argv[1]: Input JSON file e.g. data.json
#argv[2]: Output CSV file e.g. data.csv

3. preprocessor.py
-> Code to return the features in learnable formats e.g. usernames as unique IDs
#argv[1]: The file with all data i.e. output of parser.py e.g. data.csv
#argv[2]: Input unprocessed file e.g. inFile.csv <This assumes you manually split your raw data into training and test datasets after labelling>
#argv[3]: Output file for processed data e.g. outFile.csv

4. eda.py
-> Code to do visualisations
#argv[1]: Processed Training data CSV file i.e. output of preprocessor.py e.g. outFile.csv

5. model.py
-> Our machine learning model
#argv[1] : Processed training set 
#argv[2] : Processed test set
#argv[3] : Processed unlabeled set

6. data/ 
-> All the data files used for this post
#conversionTable.csv - CSV file matching each username to a unique ID
#fulldata.csv - CSV file containing all the tweets, labelled
#labeled.csv, unlabeled.csv - CSV files with labeled and unlabeled tweets, respectively
#meta.csv - An informational CSV file
#preds.csv - Output of the model, matching a user ID to their tweet's sentiment
#processedLabeled.csv, processedTest.csv, processedTrain.csv, processedUnlabeled.csv - The preprocessed data 
#project1data.csv - Unlabeled CSV file of all the tweets collected, with relevant features only
#project1data.json - The output of drinking from the Twitter API. Raw JSON objects with all features
#test.csv, train.csv, unlabeled.csv - project1data.csv split appropriately after manually labeling the data