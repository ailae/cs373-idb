#!/usr/bin/python

import ast
import requests

json = open('songs.txt', 'r').read()
songs = ast.literal_eval(json)
artist_ids = set()
for song in songs :
	artist_id = song['artist_id']
	artist_ids.add(str(song['artist_id']))
	
artist_dicts = list()
for artist_id in artist_ids :
	url = 'https://api.spotify.com/v1/artists/' + artist_id
	response = requests.get(url)
	artist = response.json()
	
	our_artist_dict = dict()
	our_artist_dict['name'] = artist['name']
	our_artist_dict['num_followers'] = artist['followers']['total']
	our_artist_dict['artist_id'] = artist['id']
	if len(artist['images']) > 0 :
		our_artist_dict['image_url'] = artist['images'][0]['url']
	else :
		our_artist_dict['image_url'] = None
	our_artist_dict['popularity'] = artist['popularity']
	artist_dicts += [our_artist_dict]
	
f = open('artists.txt', 'w')
f.write(str(artist_dicts))
f.close()
