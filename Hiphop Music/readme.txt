* Each file can be run from the terminal without needing to change the code.
* All input and output files are assumed to be located inside and will be written into 'data/'
* When running each file, the command is of the following format 'python code.py aFileHere anotherFileHere anExtraFile'
	- Henceforth, the first file after code.py is argv[1], the second argv[2] and so forth


1. LyricCrawler/
-> Scrapy spider to crawl metrolyrics.com and extract songs 
#Uses normal 'scrapy crawl spiderName -o outFile.json'  to run

2. eda.py
-> Cleaner and EDA
#argv[1]: Lyrics data file


. data/ 
-> All the data files used for this post
# lyrics.json - Objects describing songs off metrolyrics.com
# forChart.csv - Artist activity grouped by year
# AFINN.txt - List of english words rated for valence, between -5 and +5