from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlclchemy.orm import relationship, backref, joinedload_all
from sqlclchemy.orm.collections import attribute_mapped_collection

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Image() :
	def __init__(self, height, width, URL) :
		self.height = height
		self.width = weight
		self.URL = URL


class Artist(db.Model) :
	__tablename__ = 'Artist'

	name = db.Column(db.String(50), primary_key=True)
    image = db.Column(JSON)
	genre = db.Column(db.Arry[String], nullable=False)
	popularity = db.Column(db.Integer, nullable=False)
	top_tracks = db.Column(db.dict)
	spotify_url = db.Column(db.String(150), nullable=False)

	def __init__(self, name, image, genre, popularity = 0, \
		topTracks, spotifyUrl) :
	    self.name = name
	    self.image = image
	    self.genre = genre
	    self.popularity = popularity
	    self.top_tracks = top_tracks
	    self.spotify_url = spotify_url

	def __repr__(self) :
		return "Artist(name=%r, image=%r, genre=%r, popularity=%r, topTracks=%r, spotifyUrl=%r)" % (
					self.name, 
					self.image, 
					self.genre, 
					self.popularity,
					self.topTracks,
					self.spotifyUrl
				)


class Year(db.Model) :
	__tablename__ = 'Year'

	year = db.Column(db.Integer, primary_key=True)
	topSong = db.Column(db.String(50), nullable=False)
	topGenre = db.Column(db.String(50), nullable=False)
	topArtist = db.Column(db.String(50), nullable=False)
	topAlbum = db.Column(db.String(50), nullable=False)

	def __init__(self, year, topSong, topGenre, topArtist, topAlbum) :
		self.year = year
		self.topSong = topSong
		self.topGenre = topGenre
		self.topArtist = topArtist
		self.topAlbum = topAlbum


class Song(db.Model) :
	__tablename__ = 'Song'

	name = db.Column(db.String(50), primary_key=True)
	artist = db.Column(db.String(50))
	album = db.Column(db.String(50))
	explicit = db.Column(db.Boolean)
	popularity = db.Column(db.Integer)
	spotifyUrl = db.Column(db.String(150))

	def __init__(self, name, artist, album, explicit, popularity, spotifyUrl) :
		self.name = name
		self.artist = artist
		self.album = album
		self.explicit = explicit
		self.popularity = popularity
		self.spotifyUrl = spotifyUrl

class Genre(db.Model) :
	__tablename__ = 'genre'

	name = db.Column(db.String)

