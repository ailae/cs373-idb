#!/usr/bin/python
import urllib
import ast
import requests
import operator
import copy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


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
            # .strip().split(" featuring")[0]            
            unisong = song['song_name'].split("\n")[0].split("featuring ")[0].lower()
            uniartist = song['song_artist'].split("\n")[0].lower()
            def compare_names(s):
                condition_a = s['song_name'].lower().split(" -")[0].split("\n")[0].startswith(unisong)
                condition_b = unisong.startswith(s['song_name'].lower())
                condition_c = s['artist_name'].lower().split("\n")[0].split("(feat.")[0].startswith(uniartist)
                condition_d = uniartist.startswith(s['artist_name'].lower())
                return (condition_a or condition_b) and (condition_c or condition_d)

            file_song = list(filter(compare_names, song_ids))
            if file_song:
                song['song_name'] = list(file_song)[0]['song_name']
                song['song_artist'] = list(file_song)[0]['artist_name']
                song['song_id'] = list(file_song)[0]['song_id']
                song['artist_id'] = list(file_song)[0]['artist_id']
            else:                     
                max_song_ratio = 0
                max_artist_ratio = 0
                max_song = None
                for new_song in song_ids:
                    song_ratio = fuzz.ratio(new_song['song_name'].split("(feat.")[0].split(" -")[0].split("featuring ")[0], unisong)
                    artist_ratio = fuzz.ratio(new_song['artist_name'], uniartist)
                    if song_ratio + artist_ratio > max_song_ratio + max_artist_ratio:
                        max_song_ratio = song_ratio
                        max_artist_ratio = artist_ratio
                        max_song = new_song
                if max_song_ratio + max_artist_ratio >= 130 and not (max_song_ratio < 50 or max_artist_ratio < 50):
                    song['song_name'] = max_song['song_name']
                    song['song_artist'] = max_song['artist_name']
                    song['song_id'] = max_song['song_id']
                    song['artist_id'] = max_song['artist_id']                    
                else:
                    # print((unisong, max_song['song_name'], uniartist, max_song['artist_name'], max_song_ratio, max_artist_ratio))    
                    song['song_id'] = ""
                    song['artist_id'] = ""
            year_dict['song_list'] += [song]

years += [copy.deepcopy(year_dict)]
f = open('all_songs_association.txt', 'w')
f.write(str(years))
f.close()
