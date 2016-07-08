#!/usr/bin/python

import requests
from requests.utils import quote

song_dicts = list()
missing_songs = open('missing_songs.txt', 'w')

year = 0
while True :
	line = raw_input()
	line_array = line.split('\t')
	if len(line_array) == 1 :
		if year != 0 :
			missing_songs.write('\n')
			
		year = line
		missing_songs.write(str(year)+'\n')
		
		print(year)
	else :
		rank = line_array[0]
		song = line_array[1]
		artist = line_array[2]
		
		url = 'https://api.spotify.com/v1/search?type=track&q=track:'+song+' artist:'+artist+' year:'+str(year)+'&limit=1'
		url = url.replace('%', '%25')
		url = url.replace(' ', '%20')
		
		while True :
			try :
				response = requests.get(url)
				json = response.json()
				break
			except :
				print("Failed: " + url)

		items = json['tracks']['items']
		if len(items) == 0 :
			missing_songs.write(line+ ' ' + url + '\n')
			continue
		
		song = items[0]
		our_song_dict = dict()
		our_song_dict['name'] = song['name']
		our_song_dict['artist'] = song['artists'][0]['id']
		our_song_dict['album'] = song['album']['name']
		our_song_dict['explicit'] = song['explicit']
		our_song_dict['popularity'] = song['popularity']
		our_song_dict['spotify_url'] = song['uri']
		song_dicts += [our_song_dict]
		
	if not line :
		break

f = open('songs.json', 'w')
f.write(str(song_dicts))
f.close()

missing_songs.close()
