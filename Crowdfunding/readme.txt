* Each file can be run from the terminal without needing to change the code.
* All input and output files are assumed to be located inside and will be written into 'data/'
* When running each file, the command is of the following format 'python code.py aFileHere anotherFileHere anExtraFile'
	- Henceforth, the first file after code.py is argv[1], the second argv[2] and so forth


1. indiegogoWrangler.py
-> Bot that converts the CSV file containing Indiegogo projects (as of Feb 2018) at goo.gl/6pPCJb
#argv[1]: The downloaded CSV file e.g. indie.csv
#argv[2]: The JSON file to store the needed project objects returned e.g. data.json 

2. KickstarterWrangler/
-> Scrapy spider to crawl kickstarter.com and extract projects 
#Uses normal 'scrapy crawl spiderName -o outFile.json'  to run

3. indieVSkick.py
-> Visualisation of Indiegog vs Kickstarter characteristics
#argv[1]: Kickstarter data file e.g. kickCleaned.json
#argv[2]: Indiegogo data file e.g. indieCleaned.json

4. eda.py
-> EDA for Kickstarter data only
#argv[1]: Kickstarter data file

5. preprocessor.py
-> Prepares features for use in classifier e.g. removing stopwords
#argv[1]: Kickstarter data file
#argv[2]: Data file to write processed data to 

6. model.py
-> Classifier!!!
#argv[1]: Labeled processed Kickstarter data
#argv[2]: Unlabeled processed Kickstarter data
#argv[3]: Output file for labels

7. data/ 
-> All the data files used for this post
#indieDump.csv - Raw Indiegogo projects data
#kickDump.json - Raw Kickstarter projects data
#indieCleaned.json - Indiegogo data with relevant features extracted and redundancy removed
#kickCleaned.json - Kickstarter data with relevant features extracted and redundancy removed
#processedKick.json - Kickstarter data after preprocessing
#processedUnlabeled.json - Kickstarter unlabeled data for predicting
#kickUnlabeled.json - Kickstarter unlabeled data before processing
#countries.csv - Countries vs # of campaigns. Used in Tableau for visualisation