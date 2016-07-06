"""
This module demonstrates a model of our datebase used by sweetify.me
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY

BASE = declarative_base()


class Artist(BASE):

    """
    Database model of table 'Artist', which stores:
        name: the name of the artist
        image_url: a link to the artist's picture on Spotify
        genres: an array of genres the artist is associated with
        popularity: the popularity of the artist (as measured by Spotify)
        top_songs_id__name_pair: an array of the name/id pairs of all of the artist's\
                                 songs we have in our database
        spotify_url: the url to the artist's Spotify page
    """

    __tablename__ = 'Artist'

    name = Column(String(50), primary_key=True)
    image_url = Column(String(300))
    genres = Column(ARRAY(String), ForeignKey('Genre.name'))
    popularity = Column(Integer)
    top_songs_id_name_pair = Column(ARRAY(String))
    spotify_url = Column(String(300))

    def __repr__(self):
        return 'Artist(name={}, image_url={}, genre='.format(
            self.name,
            self.image_url,
        ) + self.genres + \
            ', popularity={}, spotifyUrl={}, topTracks='.format(
                self.popularity,
                self.spotifyUrl) \
            + self.top_songs_id_name_pair + ')'


class Year(BASE):

    """
    Database model of table 'Year', which stores:
        year: the year's number (ex: 2000)
        top_songs_id_name_pair: an array of the names/ids of the top 100 songs of that year
        top_genre: the genre of the top song of the year
        top_artist: the artist of the top song of the year
        top_album: the top selling album of the year (not necessarily related\
                   to the top song of the year) as its name/id pair (id comes from\
                   Spotify)
    """
    __tablename__ = 'Year'

    year = Column(Integer, primary_key=True)
    top_songs_id__name_pair = Column(ARRAY(String))
    top_genre = Column(String(50), ForeignKey('Genre.name'))
    top_artist = Column(String(50), ForeignKey('Artist.name'))
    top_album = Column(String(150))

    def __repr__(self):
        return 'Year(year={}, top_songs_id_name_pair={}, top_genre={}, '.format(
            self.year,
            self.top_songs_id_name_pair,
            self.top_genre
        ) + \
            'top_artist={}, top_album={})'.format(
                self.top_artist,
                self.top_album)


class Song(BASE):

    """
    Database model of table 'Song' which stores each song's:
        id_name_pair: a string containing the song's name and Spotify ID
        artist: artist who made the song
        album: album the song comes from, as its name/id pair (id of\
               the album from Spotify)
        explict: true if the song is explicit, false if it is not
        popularity: the popularity of the song (from Spotify)
        spotify_url: a URL to the song on Spotify
    """

    __tablename__ = 'Song'

    id_name_pair = Column(String(150), primary_key=True)
    artist = Column(String(50))
    album = Column(String(150))
    explicit = Column(Boolean)
    popularity = Column(Integer)
    spotify_url = Column(String(300))

    def __repr__(self):
        return 'Song(id_name_pair={}, artist={}, album={},'.format(
            self.id_name_pair,
            self.artist,
            self.album
        ) + \
            ' explicit={}, popularity={}, spotify_url={})'.format(
                self.explicit,
                self.popularity,
                self.spotify_url)


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

    name = Column(String(50), primary_key=True)
    description = Column(String(300))
    years_on_top = Column(ARRAY(Integer))
    artists = Column(ARRAY(String))
    related_genres = Column(ARRAY(String))

    def __repr__(self):
        return 'Genre=(name={}, description={}, years='.format(
            self.name, self.description) + self.years_on_top + ', artists=' + \
            self.artists + ', related_genres=' + self.related_genres + ')'
