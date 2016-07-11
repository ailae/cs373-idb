#!/usr/bin/python

charts = open('all_billboards_charts.txt', 'r')
years = list()
for line in charts
    line_array = line.split('\t')
    if len(line_array) == 1:
        year_dict = dict()
    year_dict['year'] = line_array[0]
    year_dict['top_album_name'] = line_array[1]
    year_dict['top_album_id'] = line_array[3]
    year_dict['top_album_artist_id'] = line_array[4]
    year_dict['top_genre_name'] = ''
    years += [year_dict]
    
print(years)