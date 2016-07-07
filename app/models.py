"""
This module demonstrates a model of our datebase used by sweetify.me
"""

from sqlalchemy import create_engine, Table, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.engine.url import URL

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'ailae',
    'password': '',
    'database': 'sweetify'
}

BASE = declarative_base()

def db_connect():
    return create_engine(URL(**DATABASE))

def create_all_tables(engine):
    BASE.metadata.create_all(engine)

# A many to many association between Artists and Genres.
# artists_genres_association = Table(
ARTISTS_GENRES_ASSOCIATION = Table(
    'artists_genres',
    BASE.metadata,
    Column('genre_name', String(100), ForeignKey('Genre.name')),
    Column('artist_name', String(150), ForeignKey('Artist.name'))
)

# A many to many association between Years and Songs. Contains the rank
# that song held in that year.
# years_songs_association = Table(
YEARS_SONGS_ASSOCIATION = Table(
    'years_songs',
    BASE.metadata,
    Column('year', Integer, ForeignKey('Year.year')),
    Column('song', String(150), ForeignKey('Song.song_id')),
    Column('rank', Integer)
)

# A many to many association between Genres and their Related Genres
# related_genres_association = Table(
RELATED_GENRES_ASSOCIATION = Table(
    'genres_to_genres',
    BASE.metadata,
    Column('genre1', String(100), ForeignKey('Genre.name')),
    Column('genre2', String(100), ForeignKey('Genre.name'))
)

class Artist(BASE):

    """
    Database model of table 'Artist', which stores:
        name: the name of the artist
        num_followers: the number of followers this artist has on Spotify
        artist_id: Spotify ID of the artist
        image_url: a link to the artist's picture on Spotify
        popularity: the popularity of the artist (as measured by Spotify)
        spotify_url: the url to the artist's Spotify page
        charted_songs: all of the artist's songs we have in our database
        genres: all of the genres the artist is associated with
    """

    __tablename__ = 'Artist'

    name = Column(String(150), primary_key=True)
    num_followers = Column(Integer)
    artist_id = Column(String(150))
    image_url = Column(String(350))
    popularity = Column(Integer)
    spotify_url = Column(String(300))

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
        "'popularity': '%s', "              %  self.popularity +    \
        "'spotify_url': '%s'}}"             %  self.spotify_url

    # def __repr__(self):
    #     return "Artist(name={}, num_follower{}, artist_id={}, ".format(
    #         self.name, self.num_followers, self.artsit_id) + \
    #     'image_url={}, popularity={}, spotify_url={}'.format(
    #         self.image_url, self.popularity, self.spotify_url)


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
    top_album_name = Column(String(100))
    top_album_id = Column(String(150))
    top_genre_name = Column(String(100), ForeignKey('Genre.name'))


    # Unidirectional one to one relationship between year and top_album_artist's name
    top_album_artist_name = Column(String(100), ForeignKey('Artist.name'))

    # Many to one relationship between Years and Genre.
    top_genre = relationship("Genre", back_populates="years_on_top")

    # A many to many relationship between Songs and Years
    top_songs = relationship("Song", secondary=YEARS_SONGS_ASSOCIATION,
                             back_populates="years_charted")

    def __repr__(self):
        return 'Year(year={}, top_album_name={}, '.format(
            self.year,
            self.top_album_name
        ) + 'top_album_id={}, top_genre_name={})'.format(
            self.top_album_id,
            self.top_genre_name)


class Song(BASE):

    """
    Database model of table 'Song' which stores each song's:
        song_id: a string containing the song's Spotify ID (if the
                 song is not available on Spotify, it will be manually
                 assigned to just be the song's name and artist combined
                 into one string)
        song_name: the name of the song
        artist_name: artist who made the song
        album_name: album the song comes from, as its name/id pair (id of\
               the album from Spotify)
        explict: true if the song is explicit, false if it is not
        popularity: the popularity of the song (from Spotify)
    """

    __tablename__ = 'Song'
    song_id = Column(String(150), primary_key=True)
    song_name = Column(String(100))

    artist_name = Column(String(150), ForeignKey('Artist.name'))
    album_name = Column(String(100))
    explicit = Column(Boolean)
    popularity = Column(Integer)

    # A many to many relationship between years and songs. Songs uses this
    # to find all of the years it charted, and its rank in each of those
    # years.
    years_charted = relationship("Year", secondary=YEARS_SONGS_ASSOCIATION,
                                 back_populates="top_songs")

    # A many to one relationship between Songs and Artist.
    artist = relationship("Artist", back_populates="charted_songs")


    def __repr__(self):
        return 'Song(song_id={}, song_name={}, artist_name={}, '.format(
            self.song_id,
            self.song_name,
            self.artist_name
        ) + \
            'album_name={}, explicit={}, popularity={})'.format(
                self.album_name,
                self.explicit,
                self.popularity)


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
    description = Column(String(300))

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







