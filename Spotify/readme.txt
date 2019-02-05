* Each file can be run from the terminal without needing to change the code.
* All input and output files are assumed to be located inside and will be written into 'data/'
* When running each file, the command is of the following format 'python code.py aFileHere anotherFileHere anExtraFile'
	- Henceforth, the first file after code.py is argv[1], the second argv[2] and so forth


1. crawler.py
-> Bot to download top 200 and viral 50 off https://spotifycharts.com/ for all periods and all regions
#argv[1]: End date in YYYY-MM-DD

2. embellishment.py
-> Bot to add features (via Spotify Web API) to tracks returned by crawler.py 
#argv[1]: CSV file with the list of tracks (should have a column of Spotify IDs)





. data/ 
-> All the data files used for this post
# top200Weekly.csv - Data on tracks that were on the top 200 list every week since 22nd Dec 2016 to 30th Sept 2018 for every region
# viral50Weekly.csv - Data on tracks that were on the viral 50 list evey week since 5th Jan 2017 to 30th Sept 2018 for every region
# top200Daily.csv - Data on tracks that were on the top 200 list every day since 1st Jan 2017 to 30th Sept 2018 for every region
# viral50Daily.csv - Data on tracks that were on the viral 50 list evey day since 1st Jan 2017 to 30th Sept 2018 for every region
