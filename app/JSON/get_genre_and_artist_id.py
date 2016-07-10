#!/usr/bin/python

import ast
import requests
import csv


with open('Year_Album_Artist.txt') as f:
    reader = csv.reader(f, delimiter="\t")
    d = list(reader)

for row in d:
	album = row[1]
	artist = row[2]
	album_str = album.replace(' ', '%20')
	r = requests.get("https://api.spotify.com/v1/search?q="+album_str+"&type=album")
	try:
		print r.json()['albums']['items'][0]
	except:
		pass
	print "\n"
