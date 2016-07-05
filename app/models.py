"""
This module demonstrates a model of our datebase used by sweetify.me
"""

# from sqlalchemy.orm import relationship, backref, joinedload_all
#from postgreSQL import ARRAY
# from sqlalchemy.orm.collections import attribute_mapped_collection
# from sqlalchemy.types import JSON

# from flask import Flask
# from flask_sqlalchemy import sqlalchemy
# # import os

# app = Flask(__name__)
# # app.config.from_object(os.environ('APP_SETTINGS'))
# app.config('SQLALCHEMY_TRACK_MODIFICATIONS') = False
# db = sqlalchemy(app)

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
# from postgresql import ARRAY

BASE = declarative_base()

class Artist(BASE):
    """
    DataBASE model of table 'Artist'
    """

    __tablename__ = 'Artist'

    name = Column(String(50), primary_key=True)
    image_url = Column(String(300))
    genres = Column(ARRAY(String), ForeignKey('Genre.name'), nullable=False)
    popularity = Column(Integer, nullable=False)
    top_songs_id_name_pair = Column(ARRAY(String), nullable=True)
    # Array of id: song, like ('12345: song', '67890: song2', ...)
    spotify_url = Column(String(300), nullable=False)

    # def __init__(self, name, image_height, image_width, image_url, \
    # 	genres, spotify_url, top_songs_id_name_pair, \
    #     popularity=0):
    #     self.name = name
    #     self.image_height = image_height
    #     self.image_url = image_url
    #     self.image_width = image_width
    #     self.genres = genres
    #     self.popularity = popularity
    #     self.top_songs_id_name_pair = top_songs_id_name_pair
    #     self.spotify_url = spotify_url

    def __repr__(self):
        return 'Artist(name={}, image_url={}, genre='.format(
            self.name,
            self.image_url,
            ) + self.genres + \
            ', popularity={}, spotifyUrl={}, topTracks='.format(
                self.popularity,
                self.spotifyUrl
            ) + self.top_songs_id_name_pair + ')'


class Year(BASE):
    """
    DataBASE model of table 'Year'
    """

    __tablename__ = 'Year'

    year = Column(Integer, primary_key=True)
    top_songs_id__name_pair = Column(ARRAY(String), nullable=False)
    top_genre = Column(String(50), ForeignKey('Genre.name'), nullable=False)
    top_artist = Column(String(50), ForeignKey('Artist.name'), \
                            nullable=False)
    top_album = Column(String(50), nullable=False)

    # def __init__(self, year, top_songs_id_name_pair, top_genre, top_artist, top_album):
    #     self.year = year
    #     self.top_songs_id_name_pair = top_songs_id_name_pair
    #     self.top_genre = top_genre
    #     self.top_artist = top_artist
    #     self.top_album = top_album

    def __repr__(self):
        return 'Year(year={}, top_songs_id_name_pair={}, top_genre={}, '.format(
            self.year,
            self.top_songs_id_name_pair,
            self.top_genre
            ) + \
            'top_artist={}, top_album={})'.format(
                self.top_artist,
                self.top_album
            )


class Song(BASE):
    """
    DataBASE model of table 'Song'
    """

    __tablename__ = 'Song'

    id_name_pair = Column(String(150), primary_key=True)
    artist = Column(String(50))
    album = Column(String(50))
    explicit = Column(Boolean)
    popularity = Column(Integer)
    spotify_url = Column(String(300))

    # def __init__(self, id_name_pair, artist, album, explicit, popularity, \
    #                 spotify_url):
    #     self.id_name_pair = id_name_pair
    #     self.artist = artist
    #     self.album = album
    #     self.explicit = explicit
    #     self.popularity = popularity
    #     self.spotify_url = spotify_url

    def __repr__(self):
        return 'Song(id_name_pair={}, artist={}, album={},'.format(
            self.id_name_pair,
            self.artist,
            self.album
            ) + \
            ' explicit={}, popularity={}, spotify_url={})'.format(
                self.explicit,
                self.popularity,
                self.spotify_url
            )


class Genre(BASE):
    """
    DataBASE model of table 'Genre'
    """

    __tablename__ = 'Genre'

    name = Column(String(50), primary_key=True, nullable=False)
    description = Column(String(300), nullable=False)
    years_on_top = Column(ARRAY(Integer))
    artists = Column(ARRAY(String))
    related_genres = Column(ARRAY(String))

    # def __init__(self, name, description, years_on_top, artists, related_genres):
    #     self.name = name
    #     self.description = description
    #     self.years_on_top = years_on_top
    #     self.artists = artists
    #     self.related_genres = related_genres

    def __repr__(self):
        return 'Genre=(name={}, description={}, years='.format(
            self.name, self.description) + self.years_on_top + ', artists=' + \
            self.artists + ', related_genres=' + self.related_genres + ')'


# class Image()
#     image_height = Column(Integer)
#     image_url = Column(String(150))
#     image_width = Column(Integer)

#     def __init__(self, image_height, image_url, image_width):
#         self.image_height = image_height
#         self.image_width = image_width
#         self.image_url = image_url

#     def __repr__(self):
#         return 'Image=(height={}, width={}, URL={})'.format(
#                     self.image_height,
#                     self.image_width,
#                     self.image_url
#                 )


    # top_song_2 = Column(String, ForeignKey('Song.name'), nullable=True)
    # top_song_3 = Column(String, ForeignKey('Song.name'), nullable=True)
    # top_song_4 = Column(String, ForeignKey('Song.name'), nullable=True)
    # top_song_5 = Column(String, ForeignKey('Song.name'), nullable=True)
    # top_song_6 = Column(String, ForeignKey('Song.name'), nullable=True)
    # top_song_7 = Column(String, ForeignKey('Song.name'), nullable=True)
    # top_song_8 = Column(String, ForeignKey('Song.name'), nullable=True)
    # top_song_9 = Column(String, ForeignKey('Song.name'), nullable=True)
    # top_song_10 = Column(String, ForeignKey('Song.name'), nullable=True)

    # year_1 = Column(Integer)
    # year_2 = Column(Integer, ForeignKey('Year.year'))
    # year_3 = Column(Integer, ForeignKey('Year.year'))
    # year_4 = Column(Integer, ForeignKey('Year.year'))
    # year_5 = Column(Integer, ForeignKey('Year.year'))
    # artist_1 = Column(String(50), ForeignKey('Artist.name'))
    # artist_2 = Column(String(50), ForeignKey('Artist.name'))
    # artist_3 = Column(String(50), ForeignKey('Artist.name'))
    # artist_4 = Column(String(50), ForeignKey('Artist.name'))
    # artist_5 = Column(String(50), ForeignKey('Artist.name'))

    # related_genre_1 = Column(String(50), ForeignKey('Genre.name'))
    # related_genre_2 = Column(String(50), ForeignKey('Genre.name'))
    # related_genre_3 = Column(String(50), ForeignKey('Genre.name'))
    # related_genre_4 = Column(String(50), ForeignKey('Genre.name'))
    # related_genre_5 = Column(String(50), ForeignKey('Genre.name'))
    # related_genres = Column(ARRAY(String))

    # def __init__(self, name, description, \
    #     year_1 = None, artist_1 = None, related_genre_1 = None, \
    #     year_2 = None, artist_2 = None, related_genre_2 = None, \
    #     year_3 = None, artist_3 = None, related_genre_3 = None, \
    #     year_4 = None, artist_4 = None, related_genre_4 = None, \
    #     year_5 = None, artist_5 = None, related_genre_5 = None):

    #     self.name = name
    #     self.year_1 = year_1
    #     self.year_2 = year_2
    #     self.year_3 = year_3
    #     self.year_4 = year_4
    #     self.year_5 = year_5
    #     self.artist_1 = artist_1
    #     self.artist_2 = artist_2
    #     self.artist_3 = artist_3
    #     self.artist_4 = artist_4
    #     self.artist_5 = artist_5
    #     self.description = description
    #     self.related_genre_1 = related_genre_1
    #     self.related_genre_2 = related_genre_2
    #     self.related_genre_3 = related_genre_3
    #     self.related_genre_4 = related_genre_4
    #     self.related_genre_5 = related_genre_5



