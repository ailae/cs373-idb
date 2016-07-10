"""
This module demonstrates a model of our datebase used by sweetify.me
"""

from sqlalchemy import create_engine, Table, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.engine.url import URL

import settings

BASE = declarative_base()

def db_connect():
    return create_engine(URL(**settings.DATABASE))

def create_all_tables(engine):
    BASE.metadata.create_all(engine)

# A many to many association between Artists and Genres.
# artists_genres_association = Table(
ARTISTS_GENRES_ASSOCIATION = Table(
    'artists_genres',
    BASE.metadata,
    Column('genre_name', String(100), ForeignKey('Genre.name')),
    Column('artist_id', String(150), ForeignKey('Artist.artist_id'))
)


# A many to many association between Genres and their Related Genres
# related_genres_association = Table(
RELATED_GENRES_ASSOCIATION = Table(
    'genres_to_genres',
    BASE.metadata,
    Column('genre1', String(100), ForeignKey('Genre.name')),
    Column('genre2', String(100), ForeignKey('Genre.name'))
)

# A many to many association between Years and Songs. Contains the rank
# that song held in that year.
class Years_Songs_Association(BASE):
    __tablename__ = 'years_songs_association'

    # Some unique id for this association
    assoc_id = Column(Integer, primary_key=True, autoincrement=True)
    
    year_num = Column('year', Integer, ForeignKey('Year.year'))
    song_id = Column('song', String(150), ForeignKey('Song.song_id'))
    rank = Column('rank', Integer)
    year = relationship("Year", back_populates="top_songs")
    song = relationship("Song", back_populates="years_charted")



class Artist(BASE):

    """
    Database model of table 'Artist', which stores:
        name: the name of the artist
        num_followers: the number of followers this artist has on Spotify
        artist_id: Spotify ID of the artist
        image_url: a link to the artist's picture on Spotify
        popularity: the popularity of the artist (as measured by Spotify)
        charted_songs: all of the artist's songs we have in our database
        genres: all of the genres the artist is associated with
    """

    __tablename__ = 'Artist'

    artist_id = Column(String(150), primary_key=True)
    name = Column(String(150))
    num_followers = Column(Integer)
    image_url = Column(String(350))
    popularity = Column(Integer)

    # Bidirectional one to many relationship between artists and songs.
    charted_songs = relationship("Song", back_populates="artist")

    # Many to many relationship.
    genres = relationship('Genre', secondary=ARTISTS_GENRES_ASSOCIATION,
                          back_populates="artists")

    def __repr__(self):
        return "{'Artist': {'name': '%s', " %  self.name +          \
        "'num_followers': '%s', "           %  self.num_followers + \
        "'artist_id': '%s', "               %  self.artist_id +     \
        "'image_url': '%s', "               %  self.image_url +     \
        "'popularity': '%s', "              %  self.popularity
        
    def dictify(self) :
        artist_dict = dict()
        artist_dict['artist_id'] = self.artist_id
        artist_dict['name'] = self.name
        artist_dict['num_followers'] = self.num_followers
        artist_dict['image_url'] = self.image_url
        artist_dict['popularity'] = self.popularity
        artist_dict['charted_songs'] = [song.dictify() for song in self.charted_songs]
        artist_dict['genres'] = [genre.dictify() for genre in self.genres]
        return artist_dict


class Year(BASE):

    """
    Database model of table 'Year', which stores:
        year: the year's number
        top_album_name: the name of the top album
        top_album_id: the Spotify id of the top album
        top_genre_name: the name of the genre of the top song
        top_album_artist_name: the name of the artist who made the
                               top album
        top_genre: a relationship that marks this year as one of the
                   ones in which this genre had a top song
        top_songs: The top 100 songs of that year
    """
    __tablename__ = 'Year'

    year = Column(Integer, primary_key=True)
    top_album_name = Column(String(250))
    top_album_id = Column(String(150))
    top_genre_name = Column(String(100), ForeignKey('Genre.name'))


    # Unidirectional one to one relationship between year and top_album_artist's name
    top_album_artist_id = Column(String(100), ForeignKey('Artist.artist_id'))

    # Many to one relationship between Years and Genre.
    top_genre = relationship("Genre", back_populates="years_on_top")

    # A many to many relationship between Songs and Years
    top_songs = relationship("Years_Songs_Association", back_populates="year")

    def __repr__(self):
        return 'Year(year={}, top_album_name={}, '.format(
            self.year,
            self.top_album_name
        ) + 'top_album_id={}, top_genre_name={})'.format(
            self.top_album_id,
            self.top_genre_name)
            
    def dictify(self) :
        year_dict = dict()
        year_dict['year'] = self.year
        year_dict['top_album_name'] = self.top_album_name
        year_dict['top_album_id'] = self.top_album_id
        year_dict['top_genre_name'] = self.top_genre_name
        year_dict['top_album_artist_id'] = self.top_album_artist_id
        year_dict['top_genre'] = self.top_genre.dictify()
        year_dict['top_songs'] = [song.dictify() for song in self.top_songs]
        return year_dict


class Song(BASE):

    """
    Database model of table 'Song' which stores each song's:
        song_id: a string containing the song's Spotify ID
        song_name: the name of the song
        artist_name: artist who made the song
        album_name: album the song comes from
        explict: true if the song is explicit, false if it is not
        popularity: the popularity of the song (from Spotify)
    """

    __tablename__ = 'Song'
    song_id = Column(String(150), primary_key=True)
    song_name = Column(String(250))

    artist_name = Column(String(150))
    artist_id = Column(String(150), ForeignKey('Artist.artist_id'))
    album_name = Column(String(250))
    explicit = Column(Boolean)
    popularity = Column(Integer)

# EDIT THIS FOR THE ASSOCIATION OBJECT CHANGE



    # A many to many relationship between years and songs. Songs uses this
    # to find all of the years it charted, and its rank in each of those
    # years.
    years_charted = relationship("Years_Songs_Association", back_populates="song")


    # A many to one relationship between Songs and Artist.
    artist = relationship("Artist", back_populates="charted_songs")


    def __repr__(self):
        return 'Song(song_id={}, song_name={}, artist_name={}, artist_id={},'.format(
            self.song_id,
            self.song_name,
            self.artist_name,
            self.artist_id
        ) + \
            'album_name={}, explicit={}, popularity={})'.format(
                self.album_name,
                self.explicit,
                self.popularity)
                
    def dictify(self):
        song_dict = dict()
        song_dict['song_id'] = self.song_id
        song_dict['song_name'] = self.song_name
        song_dict['artist_name'] = self.artist_name
        song_dict['artist_id'] = self.artist_id
        song_dict['album_name'] = self.album_name
        song_dict['explicit'] = self.explicit
        song_dict['popularity'] = self.popularity
        song_dict['years_charted'] = self.years_charted
        return song_dict


class Genre(BASE):

    """
    Database model of table 'Genre' which has:
        name: genre's name
        description: genre's description
        years_on_top: all of the years in which this genre had the #1 song
        artists: all of the artists who have been associated with this genre
        related_genres: all of the genres that have been associated with this genre
    """

    __tablename__ = 'Genre'

    name = Column(String(100), primary_key=True)
    description = Column(String(1500))

    # One to many relationship between Genre and Years.
    years_on_top = relationship("Year", back_populates="top_genre")

    # Many to many relationship between Artists and Genres.
    artists = relationship('Artist', secondary=ARTISTS_GENRES_ASSOCIATION,
                           back_populates="genres")

    # Many to many relationship between this Genre and other Genres.
    related_genres = relationship('Genre', secondary=RELATED_GENRES_ASSOCIATION,
                                  back_populates="related_genres", primaryjoin=(RELATED_GENRES_ASSOCIATION.c.genre1 == name), 
                                  secondaryjoin=(RELATED_GENRES_ASSOCIATION.c.genre2 == name))

    def __repr__(self):
        return 'Genre=(name={}, description={})'.format(
            self.name, self.description)
            
    def dictify(self) :
        genre_dict = dict()
        genre_dict['name'] = self.name
        genre_dict['description'] = self.description
        genre_dict['years_on_top'] = self.years_on_top
        genre_dict['artists'] = self.artists
        genre_dict['related_genres'] = self.related_genres
        return genre_dict
        
