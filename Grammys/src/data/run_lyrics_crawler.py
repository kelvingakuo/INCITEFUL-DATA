import subprocess

def runCrawler():
	command = 'cd LyricsFreakCrawler/LyricsFreakCrawler/ && scrapy crawl lyricsfreak -o lyrics.json'

	process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, shell = True)
	output, error = process.communicate()


