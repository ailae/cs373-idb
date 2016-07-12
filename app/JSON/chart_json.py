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
            song['song_artist'] = line_array[2].strip().split(" featuring")[0]
            unisong = unicode(song['song_name'].lower(), 'utf-8')
            uniartist = unicode(song['song_artist'].lower(), 'utf-8')
            def compare_names(s):
                condition_a = s['song_name'].lower().startswith(unisong)
                condition_b = unisong.startswith(s['song_name'].lower())
                condition_c = s['artist_name'].lower().startswith(uniartist)
                condition_d = uniartist.startswith(s['artist_name'].lower())
                return (condition_a or condition_b) and (condition_c or condition_d)
            file_song = filter(compare_names, song_ids)
            if file_song:
                song['song_name'] = file_song[0]['song_name']
                song['song_artist'] = file_song[0]['artist_name']
                song['song_id'] = file_song[0]['song_id']
                song['artist_id'] = file_song[0]['artist_id']
            else:
                song['song_id'] = ""
                song['artist_id'] = ""    
            year_dict['song_list'] += [song]

years += [copy.deepcopy(year_dict)]
f = open('all_songs_association.txt', 'w')
f.write(str(years))
f.close()
