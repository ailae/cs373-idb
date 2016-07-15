from sqlalchemy import create_engine, Table, Column, ForeignKey, Integer, \
    String, Boolean, Index, DDL, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.engine.url import URL
from sqlalchemy.types import UserDefinedType

import settings

BASE = declarative_base()


def db_connect():
    """
    Function used to connect to the database specified in the settings file.
    """
    return create_engine(URL(**settings.DATABASE))


def create_all_tables(engine):
    """
    Given an engine, creates all tables for these models.
    """
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


class TsVector(UserDefinedType):
    """
    This class represents a TsVector, and it will be
    the data type of the column in each model that will
    be dedicated to search.
    This design is based on Noufal Ibrahim's guide, found
    here: http://nibrahim.net.in/2013/11/29/sqlalchemy_and_full_text_searching_in_postgresql.html
    """
    name = "TSVECTOR"

    def get_col_spec(self):
        """
        This method defines what the name of the TsVector will
        be in DDL. We are simply returning "TSVECTOR."
        """
        return self.name

class YearsSongsAssociation(BASE):

    """
    Holds associations between a Year and a Song, and stores
    the rank that song had in that year.
    """
    __tablename__ = 'yearssongsassociation'

    year_num = Column(
        'year', Integer, ForeignKey('Year.year'), primary_key=True)
    song_id = Column(
        'song', String(150), ForeignKey('Song.song_id'), primary_key=True)
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

    # TsVector column used for searching.
    tsvector_col = Column(TsVector)
    
    # Create an index for the tsvector column
    __table_args__ = (Index('artist_tsvector_idx', 'tsvector_col', postgresql_using='gin'),)

    def dictify(self):
        artist_dict = dict()
        artist_dict['artist_id'] = (self.artist_id)
        artist_dict['name'] = (self.name)
        artist_dict['num_followers'] = self.num_followers
        artist_dict['image_url'] = (self.image_url)
        artist_dict['popularity'] = self.popularity
        artist_dict['charted_songs'] = [
            (song.song_name) for song in self.charted_songs]
        artist_dict['genres'] = [(genre.name) for genre in self.genres]
        return artist_dict

# Create a trigger to check for updates to Artist and update the TsVector
# accordingly.
artist_vector_trigger = DDL("""
    CREATE TRIGGER artist_tsvector_update BEFORE INSERT OR UPDATE ON "Artist" FOR EACH ROW EXECUTE PROCEDURE
    tsvector_update_trigger(tsvector_col, 'pg_catalog.english', 'name')
    """)
event.listen(Artist.__table__, 'after_create', artist_vector_trigger.execute_if(dialect='postgresql'))

class Year(BASE):

    """
    Database model of table 'Year', which stores:
        year: the year's number
        top_album_name: the name of the top album
        top_album_id: the Spotify id of the top album
        top_genre_name: the name of the genre of the year's top album
        top_album_artist_id: the id of the artist who made the top album
        top_genre: the genre of the year's top album
        top_songs: The top 100 songs of that year
    """
    __tablename__ = 'Year'

    year = Column(Integer, primary_key=True)
    top_album_name = Column(String(250))
    top_album_id = Column(String(150))
    top_genre_name = Column(String(100), ForeignKey('Genre.name'))

    # Unidirectional one to one relationship between year and
    # top_album_artist's name
    top_album_artist_id = Column(String(100), ForeignKey('Artist.artist_id'))

    # Many to one relationship between Years and Genre.
    top_genre = relationship("Genre", back_populates="years_on_top")

    # A many to many relationship between Songs and Years
    top_songs = relationship("YearsSongsAssociation", back_populates="year")

    def dictify(self):
        year_dict = dict()
        year_dict['year'] = self.year
        year_dict['top_album_name'] = (self.top_album_name)
        year_dict['top_album_id'] = (self.top_album_id)
        year_dict['top_genre_name'] = (self.top_genre_name)
        year_dict['top_album_artist_id'] = (self.top_album_artist_id)
        year_dict['top_songs'] = [
            assoc.song.song_name for assoc in self.top_songs]
        return year_dict


class Song(BASE):

    """
    Database model of table 'Song' which stores each song's:
        song_id: a string containing the song's Spotify ID
        song_name: the name of the song
        artist_name: artist who made the song
        artist_id: the id of the artist who made the song
        album_name: album the song comes from
        explict: true if the song is explicit, false if it is not
        popularity: the popularity of the song (from Spotify)
        years_charted: years in which this song was in the top chart
        artist: the object of the artist who made the song
    """

    __tablename__ = 'Song'
    song_id = Column(String(150), primary_key=True)
    song_name = Column(String(250))

    artist_name = Column(String(150))
    artist_id = Column(String(150), ForeignKey('Artist.artist_id'))
    album_name = Column(String(250))
    explicit = Column(Boolean)
    popularity = Column(Integer)

    # A many to many relationship between years and songs. Songs uses this
    # to find all of the years it charted, and its rank in each of those
    # years.
    years_charted = relationship(
        "YearsSongsAssociation", back_populates="song")

    # A many to one relationship between Songs and Artist.
    artist = relationship("Artist", back_populates="charted_songs")

    def dictify(self):
        song_dict = dict()
        song_dict['song_id'] = (self.song_id)
        song_dict['song_name'] = (self.song_name)
        song_dict['artist_name'] = (self.artist_name)
        song_dict['artist_id'] = (self.artist_id)
        song_dict['album_name'] = (self.album_name)
        song_dict['explicit'] = self.explicit
        song_dict['popularity'] = self.popularity
        song_dict['years_charted'] = [assoc.year_num for assoc
                                      in self.years_charted]
        return song_dict


class Genre(BASE):

    """
    Database model of table 'Genre' which has:
        name: genre's name
        description: genre's description
        years_on_top: all of the years in which this genre was the top genre
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
    related_genres = relationship(
        'Genre', secondary=RELATED_GENRES_ASSOCIATION,
        back_populates="related_genres",
        primaryjoin=(RELATED_GENRES_ASSOCIATION.c.genre1 == name),
        secondaryjoin=(RELATED_GENRES_ASSOCIATION.c.genre2 == name))

    def dictify(self):
        genre_dict = dict()
        genre_dict['name'] = (self.name)
        genre_dict['description'] = (self.description)
        genre_dict['years_on_top'] = [year.year for year in self.years_on_top]
        genre_dict['artists'] = [(artist.name) for artist in self.artists]
        genre_dict['related_genres'] = [
            (genre.name) for genre in self.related_genres]
        return genre_dict