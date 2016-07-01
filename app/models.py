from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import relationship, backref, joinedload_all
from postgreSQL import ARRAY
from sqlalchemy.orm.collections import attribute_mapped_collection
# from sqlalchemy.types import JSON

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Artist(db.Model) :
	__tablename__ = 'Artist'

	name = db.Column(db.String(50), primary_key=True)
	image_height = db.Column(db.Integer)
	image_url = db.Column(db.String(150))
	image_width = db.Column(db.Integer)
	genre = db.Column(db.ARRAY[String], ForeignKey('Genre.name'), nullable=False)
	popularity = db.Column(db.Integer, nullable=False)
	top_songs = db.Column(db.ARRAY[String], nullable=True)
	spotify_url = db.Column(db.String(150), nullable=False)

	def __init__(self, name, image_url, genre, spotify_url, top_songs, \
		popularity=0) :
	    self.name = name
	    self.image_height = image_height
	    self.image_url = image_url
	    self.image_width = image_width
	    self.genre = genre
	    self.popularity = popularity
	    self.top_songs = top_songs
	    self.spotify_url = spotify_url

	def __repr__(self) :
		return 'Artist(name={}, image_url={}, genre='.format(
					self.name, 
					self.image_url, 
					) + self.genre + \
				', popularity={}, spotifyUrl={}, topTracks='.format(
					self.popularity,
					self.spotifyUrl
				) + self.songs + ')'


class Year(db.Model) :
	__tablename__ = 'Year'

	year = db.Column(db.Integer, primary_key=True)
	top_songs = db.Column(db.ARRAY[String], ForeiginKey('Song.name'), nullable=False)
	top_genre = db.Column(db.String(50), ForeignKey('Genre.name'), nullable=False)
	top_artist = db.Column(db.String(50), ForeignKey('Artist.name'), \
							nullable=False)
	top_album = db.Column(db.String(50), nullable=False)

	def __init__(self, year, top_song, top_genre, top_artist, top_album) :
		self.year = year
		self.top_song = top_song
		self.top_genre = top_genre
		self.top_artist = top_artist
		self.top_album = top_album

	def __repr__(self) :
		return 'Year(year={}, top_song={}, top_genre={}, '.format(
					self.year,
					self.top_song,
					self.top_genre
					) + \
				'top_artist={}, top_album={})'.format(
					self.top_artist,
					self.top_album
				)


class Song(db.Model) :
	__tablename__ = 'Song'

	name = db.Column(db.String(50), primary_key=True)
	artist = db.Column(db.String(50))
	album = db.Column(db.String(50))
	explicit = db.Column(db.Boolean)
	popularity = db.Column(db.Integer)
	spotify_url = db.Column(db.String(150))

	def __init__(self, name, artist, album, explicit, popularity, \
					spotify_url) :
		self.name = name
		self.artist = artist
		self.album = album
		self.explicit = explicit
		self.popularity = popularity
		self.spotify_url = spotify_url

	def __repr__(self) :
		return 'Song(name={}, artist={}, album={},'.format(
					self.name,
					self.artist,
					self.album
					) + \
				' explicit={}, popularity={}, spotify_url={})'.format(
					self.explicit,
					self.popularity,
					self.spotify_url
					)


class Genre(db.Model) :
	__tablename__ = 'Genre'

	name = db.Column(db.String(50), primary_key=True, nullable=False)
	description = db.Column(db.String(300), nullable=False)
	years = db.Column(db.ARRAY[Integer], )	
	artists = db.Column(db.ARRAY[String])
	related_genres = db.Column(db.ARRAY[Sting])

	def __init__(self, name, description, years, artists, related_genres) : 
		self.name = name
		self.description = description
		self.years = years
		self.artists = artists
		self.related_genres = related_genres

	def __repr__(self) :
		return 'Genre=(name={}, description={}, years='.format(
			self.name, self.description) + self.years + ', artists=' + \
			self.artists + ', related_genres=' + self.related_genres + ')'


# class Image()
# 	image_height = db.Column(db.Integer)
# 	image_url = db.Column(db.String(150))
# 	image_width = db.Column(db.Integer)

# 	def __init__(self, image_height, image_url, image_width) :
# 		self.image_height = image_height
# 		self.image_width = image_width
# 		self.image_url = image_url

# 	def __repr__(self) :
# 		return 'Image=(height={}, width={}, URL={})'.format(
# 					self.image_height,
# 					self.image_width,
# 					self.image_url
# 				)


	# top_song_2 = db.Column(db.String, ForeignKey('Song.name'), nullable=True)
	# top_song_3 = db.Column(db.String, ForeignKey('Song.name'), nullable=True)
	# top_song_4 = db.Column(db.String, ForeignKey('Song.name'), nullable=True)
	# top_song_5 = db.Column(db.String, ForeignKey('Song.name'), nullable=True)
	# top_song_6 = db.Column(db.String, ForeignKey('Song.name'), nullable=True)
	# top_song_7 = db.Column(db.String, ForeignKey('Song.name'), nullable=True)
	# top_song_8 = db.Column(db.String, ForeignKey('Song.name'), nullable=True)
	# top_song_9 = db.Column(db.String, ForeignKey('Song.name'), nullable=True)
	# top_song_10 = db.Column(db.String, ForeignKey('Song.name'), nullable=True)

	# year_1 = db.Column(db.Integer)
	# year_2 = db.Column(db.Integer, ForeignKey('Year.year'))
	# year_3 = db.Column(db.Integer, ForeignKey('Year.year'))
	# year_4 = db.Column(db.Integer, ForeignKey('Year.year'))
	# year_5 = db.Column(db.Integer, ForeignKey('Year.year'))
	# artist_1 = db.Column(db.String(50), ForeignKey('Artist.name'))
	# artist_2 = db.Column(db.String(50), ForeignKey('Artist.name'))
	# artist_3 = db.Column(db.String(50), ForeignKey('Artist.name'))
	# artist_4 = db.Column(db.String(50), ForeignKey('Artist.name'))
	# artist_5 = db.Column(db.String(50), ForeignKey('Artist.name')) 

	# related_genre_1 = db.Column(db.String(50), ForeignKey('Genre.name'))
	# related_genre_2 = db.Column(db.String(50), ForeignKey('Genre.name'))
	# related_genre_3 = db.Column(db.String(50), ForeignKey('Genre.name'))
	# related_genre_4 = db.Column(db.String(50), ForeignKey('Genre.name'))
	# related_genre_5 = db.Column(db.String(50), ForeignKey('Genre.name'))
	# related_genres = db.Column(db.ARRAY[String])

	# def __init__(self, name, description, \
	# 	year_1 = None, artist_1 = None, related_genre_1 = None, \
	# 	year_2 = None, artist_2 = None, related_genre_2 = None, \
	# 	year_3 = None, artist_3 = None, related_genre_3 = None, \
	# 	year_4 = None, artist_4 = None, related_genre_4 = None, \
	# 	year_5 = None, artist_5 = None, related_genre_5 = None) :

	# 	self.name = name
	# 	self.year_1 = year_1
	# 	self.year_2 = year_2
	# 	self.year_3 = year_3
	# 	self.year_4 = year_4
	# 	self.year_5 = year_5
	# 	self.artist_1 = artist_1
	# 	self.artist_2 = artist_2
	# 	self.artist_3 = artist_3
	# 	self.artist_4 = artist_4
	# 	self.artist_5 = artist_5
	# 	self.description = description
	# 	self.related_genre_1 = related_genre_1
	# 	self.related_genre_2 = related_genre_2
	# 	self.related_genre_3 = related_genre_3
	# 	self.related_genre_4 = related_genre_4
	# 	self.related_genre_5 = related_genre_5



