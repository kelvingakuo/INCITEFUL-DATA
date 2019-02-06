import subprocess

def runCrawler(what):
	if(what == 'lyrics'):
		command = 'cd LyricsFreakCrawler/LyricsFreakCrawler/ && scrapy crawl lyricsfreak -o lyrics.json'
	elif(what == 'artistData'):
		command = 'cd WikipediaCrawler/WikipediaCrawler/ && scrapy crawl artistInfo -o artist_data.json'

	process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, shell = True)
	output, error = process.communicate()


