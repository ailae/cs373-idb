#!/usr/bin/python
import urllib2
import ast
import requests
import operator
import copy

years = list()
year_dict = dict()
json = open('songs.txt', 'r').read()
song_ids = ast.literal_eval(json)
year_dict['year'] = 1990
year_dict['song_list'] = []
with open('all_billboard_charts.txt', 'r') as f:
    for line in f:    
        line_array = line.split('\t')
        if len(line_array[0]) > 3:
            years += [copy.deepcopy(year_dict)]
            year_dict = dict()
            year_dict['year'] = line
            year_dict['song_list'] = []
        else:
            song = dict()
            song['rank'] = line_array[0]
            song['song_name'] = line_array[1]
            song['song_artist'] = line_array[2]
            file_song = filter(lambda s: s['song_name'] == unicode(line_array[1], 'utf-8'), song_ids)
            if file_song:
                song['song_id'] = str(file_song[0]['song_id'])
                song['artist_id'] = str(file_song[0]['artist_id'])
            else:
                song['song_id'] = ""
                song['artist_id'] = ""    
            year_dict['song_list'] += [song]

f = open('all_songs_association.txt', 'w')
f.write(str(years))
f.close()
