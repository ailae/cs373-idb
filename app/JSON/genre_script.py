#!/usr/bin/python
import urllib2
import ast
import requests
import operator

json = open('artist_genres.txt', 'r').read()
artists = ast.literal_eval(json)
totals = dict()
artist_genres = list()

# for artist in artists:
# 	uppercase_list = list()
# 	for genre in artist['genres']:
# 		uppercase_list += [' '.join(s[0].upper() + s[1:] for s in genre.split())]
# 	artist['genres'] = uppercase_list	
# for artist in artists:
# 	for genre in artist['genres']:
# 		if genre in totals:
# 			totals[genre] = totals[genre] + 1
# 		else:
# 			totals[genre] = 1

# print str(sorted(totals.items(), key=operator.itemgetter(1), reverse=True))
# f = open('artist_genres.txt', 'w')
# f.write(str(artists))
# f.close()

empty_dicts = list()
genre_set = set()

for artist in artists:
	if 'Alternative' in artist['genres']:
		artist['genres'].remove('Alternative')
		if 'Alternative Rock' not in artist['genres']:
			artist['genres'] += ['Alternative Rock']
# for genre in genre_set:
# 	empty_dicts += [{'name' : genre, 'related' : []}]
# 	print genre
	# json = requests.get("http://ws.audioscrobbler.com/2.0/?method=tag.getinfo&tag=" + genre + "&api_key=5da0c4646700667bf92c6faa09a6c909&format=json").json()
	# descriptions += [{'name' : genre, 'summary' : json['tag']['wiki']['summary'], 'content' : json['tag']['wiki']['content']}]

f = open('artist_genres.txt', 'w')
f.write(str(artists))
f.close()
