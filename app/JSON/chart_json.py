#!/usr/bin/python

charts = open('')
years = list()
while True :
    line = raw_input()
    if not line :
        break
    
    line_array = line.split('\t')
    
    year_dict = dict()
    year_dict['year'] = line_array[0]
    year_dict['top_album_name'] = line_array[1]
    year_dict['top_album_id'] = line_array[3]
    year_dict['top_album_artist_id'] = line_array[4]
    year_dict['top_genre_name'] = ''
    years += [year_dict]
    
print(years)