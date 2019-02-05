import json
import csv
import sys

print('Reading JSON...')

with open('data/'+sys.argv[1], 'r') as dump:
	data = json.load(dump)
print('JSON locked and loaded!!')

print('Parsing begins...')

with open('data/'+sys.argv[2], 'a') as dump:
	writer = csv.writer(dump) 
	writer.writerow(['id', 'date', 'quotes', 'retweets', 'favourites', 'username', 'followers', 'isVerified' ,'ppicURL', 'text'])
	for tweet in data['TweetData']:
		#Tweet Properties
		tweetId = tweet.get('id_str')
		date = tweet.get('created_at')

		text = tweet.get('full_text').encode('ascii','ignore').decode('ascii')

		if(tweet.get('quote_count') is not None):
			quotes = tweet.get('quote_count')
		else:
			quotes = 0

		if(tweet.get('retweet_count') is not None):
			retweets = tweet.get('retweet_count')
		else:
			retweets = 0

		if(tweet.get('favorite_count') is not None):
			favourites = tweet.get('favorite_count')
		else:
			favourites = 0

		#User Properties

		userObj = tweet.get('user', {})

		username = '@' + userObj.get('screen_name')

		followers = userObj.get('followers_count')

		isVerified = userObj.get('verified')

		ppicURL = userObj.get('profile_image_url')

		writer.writerow([tweetId, date, quotes, retweets, favourites, username, followers, isVerified ,ppicURL, text])

print('Parsing completed successfully. {} rows created.'.format(len(data['TweetData'])))

