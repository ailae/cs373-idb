#!/usr/bin/python
import urllib2
import ast
import requests

json = open('artists.txt', 'r').read()
artists = ast.literal_eval(json)
artist_genres = list()

for artist in artists:
	try:
		name = artist['name']
		name.replace(" ", "")	
		url = "http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist=" + name + "&api_key=5da0c4646700667bf92c6faa09a6c909&format=json"
		tags = requests.get(url).json()	
		if tags['toptags']['tag']:
			artist_genres += [{'name' : name, 'genres' : [tags['toptags']['tag'][0]['name'], tags['toptags']['tag'][1]['name'], tags['toptags']['tag'][2]['name']]}]
	except:
		artist_genres += [{'name' : name, 'genres' : ['no genre given']}]
	# 	pass
f = open ('artist_genres.txt', 'w')
f.write(str(artist_genres))
f.close()		
	# genres.add()
# for genre in genres :
# 	try:
# 		url = "http://ws.audioscrobbler.com/2.0/?method=tag.getinfo&tag=disco&api_key=YOUR_API_KEY&format=json"
# 		req = urllib2.Request(url, headers=header)
# 		page = urllib2.urlopen(url)
# 		soup = BeautifulSoup(page)
	
# 	our_genre_dict = dict()
# 	our_genre_dict['name'] = genre
# 	our_artist_dict['num_followers'] = artist['followers']['total']
# 	our_artist_dict['artist_id'] = artist['id']
# 	if len(artist['images']) > 0 :
# 		our_artist_dict['image_url'] = artist['images'][0]['url']
# 	else :
# 		our_artist_dict['image_url'] = None
# 	our_artist_dict['popularity'] = artist['popularity']
# 	artist_dicts += [our_artist_dict]
	
# f = open('artists.txt', 'w')
# f.write(str(artist_dicts))
# f.close()
