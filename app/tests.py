#!/usr/bin/env python3
"""
Tests.py - Contains unit tests to check the validity of all of our
database's models: Artist, Year, Song, and Genre.
"""

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import Artist, Year, Song, Genre


class ModelUnitTests(unittest.TestCase):

    """
    ModelUnitTests will create a new database in memory for each
    test and verify that adding entries and querying for them will
    return expected results.
    """

    def setUp(self):
        self.base = declarative_base()
        self.engine = create_engine("sqlite:///:memory:")
        self.made_session = sessionmaker(bind=self.engine)
        self.session = self.made_session()
        self.base.metadata.create_all(self.engine)

    def tearDown(self):
        self.base.metadata.drop_all(self.engine)

    # These tests ensure that the Artist model behaves as expected.
    # Tests that once the instance is added to the database, it is found
    # and checks that one of its attributes returns the specified value.
    def test_artist_1(self):
        name = "Kanye West"
        image_url = "http://cdn.uinterview.com/wp-content/uploads/2016/02/news-kanye-west.jpg"
        genres = ["Rap", "Hip Hop"]
        popularity = 50
        top_songs = ["Blood On The Leaves:3032a29s", "Saint Pablo:30924p"]
        spotify_url = "http://www.spotify.com/kanye"
        test_artist = Artist(
            name=name, image_url=image_url, genres=genres, spotify_url=spotify_url,
            top_songs_id_name_pair=top_songs, popularity=popularity)
        self.session.add(test_artist)
        self.session.commit()
        self.assertTrue(test_artist in self.session)
        kanye = self.session.query(Artist).filter_by(name="Kanye West").first()
        kanye_image = kanye.image_url
        self.assertEqual(kanye_image, image_url)

    # Add two artists, and ensure they are in the database. Search for an artist that
    # wasn't added, and ensure that it is not found in the database.
    def test_artist_2(self):
        name = "Beyonce"
        image_url = "https://spotifyinsights.files.wordpress.com/2015/03/" + \
            "beyonce_publicityphoto6-1.jpg"
        genres = ["R&B", "Pop"]
        popularity = 80
        top_songs = ["Drunk In Love:02193a0"]
        spotify_url = "http://www.spotify.com/beyonce"
        test_artist = Artist(
            name=name, image_url=image_url, genres=genres, spotify_url=spotify_url,
            top_songs_id_name_pair=top_songs, popularity=popularity)
        name_2 = "DJ Khaled"
        image_url_2 = "https://i.scdn.co/image/ec4dd6900eb90044"
        genres_2 = ["R&B", "Hip Hop", "Rap"]
        popularity_2 = 21
        top_songs_2 = ["Hold You Down:3029802"]
        spotify_url_2 = "http://www.spotify.com/djkhaled"
        test_artist_2 = Artist(
            name=name_2, image_url=image_url_2, genres=genres_2, spotify_url=spotify_url_2,
            top_songs_id_name_pair=top_songs_2, popularity=popularity_2)
        self.session.add_all([test_artist, test_artist_2])
        self.session.commit()

        dj_khaled = self.session.query(
            Artist).filter_by(name="DJ Khaled").first()
        beyonce = self.session.query(Artist).filter_by(name="Beyonce").first()
        random_not_added = self.session.query(
            Artist).filter_by(name="random").first()
        self.assertTrue((dj_khaled is not None) and (
            beyonce is not None) and (random_not_added is None))

    # Add two artists to the database, then filter them by an attribute whose
    # value they have in common. A third artist is added as well, who doesn't share
    # the same value. Ensure that the returned filter list only has two
    # artists.
    def test_artist_3(self):
        name = "SomeArtist"
        image_url = "some_url"
        genres = ["Potato", "Tomato"]
        popularity = 100
        top_songs = ["First Song:1234", "Another Song:5678"]
        spotify_url = "http://www.spotify.com/artist"
        test_artist = Artist(
            name=name, image_url=image_url, genres=genres, spotify_url=spotify_url,
            top_songs_id_name_pair=top_songs, popularity=popularity)
        self.session.add(test_artist)

        name_2 = "AnotherArtist"
        image_url_2 = "some_url"
        genres_2 = ["Potato", "Tomato"]
        popularity_2 = 100
        top_songs_2 = ["The Song:2341", "Second Song:8567"]
        spotify_url_2 = "http://www.spotify.com/artist"
        test_artist_2 = Artist(
            name=name_2, image_url=image_url_2, genres=genres_2, spotify_url=spotify_url_2,
            top_songs_id_name_pair=top_songs_2, popularity=popularity_2)
        self.session.add(test_artist_2)

        name_3 = "Some random artist"
        image_url_3 = "some_url"
        genres_3 = ["Potato", "Tomato"]
        popularity_3 = 2
        top_songs_3 = ["Random Song:3920sid", "Random 2 Song:5678idSp"]
        spotify_url_3 = "http://www.spotify.com/artist"
        test_artist_3 = Artist(
            name=name_3, image_url=image_url_3, genres=genres_3, spotify_url=spotify_url_3,
            top_songs_id_name_pair=top_songs_3, popularity=popularity_3)
        self.session.add(test_artist_3)
        self.session.commit()

        artist_list = self.session.query(
            Artist).filter_by(popularity=100).all()
        self.assertTrue(len(artist_list) == 2)

    # The following tests check the Year model

    # Add a year to the database, verify that it can be found,
    # retrieve the top_genre from that year, and verify it matches
    # what is expected.
    def test_year_1(self):
        year = 2001
        top_songs = ["Some Really Popular Song:5423", "Some Other Song:04921"]
        top_genre = "Dubstep"
        top_artist = "NSYNC"
        top_album = "The Best Album:123098"
        test_year = Year(
            year=year, top_songs_id_name_pair=top_songs, top_genre=top_genre,
            top_artist=top_artist, top_album=top_album)
        self.session.add(test_year)
        self.session.commit()

        self.assertTrue(test_year in self.session)
        actual_year = self.session.query(Year).filter_by(year=2001).first()
        actual_top_genre = actual_year.top_genre
        self.assertEqual(top_genre, actual_top_genre)

    def test_year_2(self):
        year = 2015
        top_songs = ["New Song:19651469", "Old Song:65165162"]
        top_genre = "Pop"
        top_artist = "Some Important Artist"
        top_album = "The Biggest Album of 2015:2193810"
        test_year = Year(
            year=year, top_songs_id_name_pair=top_songs, top_genre=top_genre,
            top_artist=top_artist, top_album=top_album)
        year_2 = 2014
        top_songs_2 = ["Another New Song:5165065", "Older Song:45980515"]
        top_genre_2 = "Rap"
        top_artist_2 = "Rapper"
        top_album_2 = "The Biggest Album of 2014:201932019"
        test_year_2 = Year(
            year=year_2, top_songs_id_name_pair=top_songs_2, top_genre=top_genre_2,
            top_artist=top_artist_2, top_album=top_album_2)

        self.session.add_all([test_year, test_year_2])
        self.session.commit()

        fifteen = self.session.query(Year).filter_by(year=2015).first()
        fourteen = self.session.query(Year).filter_by(year=2014).first()
        self.assertTrue(fifteen is not None)
        self.assertTrue(fourteen is not None)
        fifteen_top_album = fifteen.top_album
        fourteen_top_album = fourteen.top_album
        correct_albums = fifteen_top_album == top_album and fourteen_top_album == top_album_2
        self.assertTrue(correct_albums)

    def test_year_3(self):
        year = 2015
        top_songs = ["New Song:9862162", "Old Song:98498216565162"]
        top_genre = "Rap"
        top_artist = "Some Important Artist"
        top_album = "The Biggest Album of 2015:212981"
        test_year = Year(
            year=year, top_songs_id_name_pair=top_songs, top_genre=top_genre,
            top_artist=top_artist, top_album=top_album)
        year_2 = 2014
        top_songs_2 = ["Another New Song:989826515", "Older Song:648915484"]
        top_genre_2 = "Rap"
        top_artist_2 = "Rapper"
        top_album_2 = "The Biggest Album of 2014:21839189"
        test_year_2 = Year(
            year=year_2, top_songs_id_name_pair=top_songs_2, top_genre=top_genre_2,
            top_artist=top_artist_2, top_album=top_album_2)
        year_3 = 2013
        top_songs_3 = ["thirteen:9216519819", "another thirteen:2151248"]
        top_genre_3 = "Pop"
        top_artist_3 = "Some dude"
        top_album_3 = "The Biggest Album of 2013:2193871764"
        test_year_3 = Year(
            year=year_3, top_songs_id_name_pair=top_songs_3, top_genre=top_genre_3,
            top_artist=top_artist_3, top_album=top_album_3)
        self.session.add_all([test_year, test_year_2, test_year_3])
        self.session.commit()

        # If we search for years who only had a top genre of rap, we should
        # only get two years, not three.
        years_list = self.session.query(Year).filter_by(top_genre="Rap").all()
        self.assertTrue(len(years_list) == 2)

    # The following tests will check the Song model
    def test_song_1(self):
        name = "A Song:99999"
        artist = "Some Artist"
        album = "Some Album:2134"
        explicit = True
        popularity = 10
        spotify_url = "www.spotify.com/some_url"
        test_song = Song(
            id_name_pair=name, artist=artist, album=album, explict=explicit,
            popularity=popularity, spotify_url=spotify_url)
        self.session.add(test_song)
        self.session.commit()

        self.assertTrue(test_song in self.session)
        this_song = self.session.query(
            Song).filter(id_name_pair="A Song:99999")
        this_song_explicit = this_song.explicit
        self.assertTrue(this_song_explicit)

    def test_song_2(self):
        name = "Some Song:123"
        artist = "Some Artist"
        album = "Some Album:3279"
        explicit = True
        popularity = 10
        spotify_url = "www.spotify.com/some_url"
        test_song = Song(
            id_name_pair=name, artist=artist, album=album, explict=explicit,
            popularity=popularity, spotify_url=spotify_url)

        name_2 = "Second Song:234"
        artist_2 = "Second Artist"
        album_2 = "Second Album:0128930"
        explicit_2 = False
        popularity_2 = 20
        spotify_url_2 = "www.spotify.com/some_other_url"
        test_song_2 = Song(
            id_name_pair=name_2, artist=artist_2, album=album_2, explict=explicit_2,
            popularity=popularity_2, spotify_url=spotify_url_2)

        self.session.add_all([test_song, test_song_2])
        self.session.commit()

        first_song = self.session.query(Song).filter_by(
            id_name_pair="Some Song:123").first()
        second_song = self.session.query(Song).filter_by(
            id_name_pair="Second Song:234").first()
        self.assertTrue(first_song is not None)
        self.assertTrue(second_song is not None)
        correct_explicits = first_song.explicit and not second_song.explicit
        self.assertTrue(correct_explicits)

    def test_song_3(self):
        name = "Some Song:123"
        artist = "The Same Artist"
        album = "The Same Album:123121"
        explicit = True
        popularity = 100
        spotify_url = "www.spotify.com/some_url"
        test_song = Song(
            id_name_pair=name, artist=artist, album=album, explict=explicit,
            popularity=popularity, spotify_url=spotify_url)

        name_2 = "Different Song Same Album:321"
        artist_2 = "The Same Artist"
        album_2 = "The Same Album:123121"
        explicit_2 = True
        popularity_2 = 99
        spotify_url_2 = "www.spotify.com/some_url_of_diff_song"
        test_song_2 = Song(
            id_name_pair=name_2, artist=artist_2, album=album_2, explict=explicit_2,
            popularity=popularity_2, spotify_url=spotify_url_2)

        name_3 = "Different Song Diff Album:444"
        artist_3 = "Diff Artist"
        album_3 = "Diff Album:08342"
        explicit_3 = False
        popularity_3 = 20
        spotify_url_3 = "www.spotify.com/totally_diff"
        test_song_3 = Song(
            id_name_pair=name_3, artist=artist_3, album=album_3, explict=explicit_3,
            popularity=popularity_3, spotify_url=spotify_url_3)

        self.session.add_all([test_song, test_song_2, test_song_3])
        self.session.commit()

        songs_list = self.session.query(Song).filter_by(
            album="The Same Album:123121").all()
        self.assertTrue(len(songs_list) == 2)
        not_songs_list = self.session.query(
            Song).filter_by(explicit=False).all()
        self.assertTrue(len(not_songs_list) == 1)

    # The following tests check the Genre model
    def test_genre_1(self):
        name = "The Genre"
        description = "Some description of the genre."
        years_on_top = [2001, 2002, 2003]
        artists = ["Artist 1", "Artist 2", "Artist 3"]
        related_genres = ["Related 1", "Related 2", "Related 3"]
        test_genre = Genre(
            name=name, description=description, years_on_top=years_on_top,
            artists=artists, related_genres=related_genres)

        self.session.add(test_genre)
        self.session.commit()

        self.assertTrue(test_genre in self.session)
        actual_genre = self.session.query(
            Genre).filter_by(name="The Genre").first()
        actual_name = actual_genre.name
        self.assertEqual(actual_name, name)

    def test_genre_2(self):
        name = "The Genre"
        description = "Some description of the genre."
        years_on_top = [2001, 2002, 2003]
        artists = ["Artist 1", "Artist 2", "Artist 3"]
        related_genres = ["Related 1", "Related 2", "Related 3"]
        test_genre = Genre(
            name=name, description=description, years_on_top=years_on_top,
            artists=artists, related_genres=related_genres)

        name_2 = "Second Genre"
        description_2 = "Second description of second genre."
        years_on_top_2 = [1999]
        artists_2 = ["Artist 1", "Artist 41", "Artist 34"]
        related_genres_2 = ["Related 18732", "Related 2", "Related 3242"]
        test_genre_2 = Genre(
            name=name_2, description=description_2, years_on_top=years_on_top_2,
            artists=artists_2, related_genres=related_genres_2)

        self.session.add_all([test_genre, test_genre_2])
        self.session.commit()

        first_genre = self.session.query(
            Genre).filter_by(name="The Genre").first()
        second_genre = self.session.query(
            Genre).filter_by(name="Second Genre").first()
        self.assertTrue(first_genre is not None)
        self.assertTrue(second_genre is not None)
        correct_descriptions = (first_genre.description ==
                                "Some description of second genre.") and \
                               (second_genre.description ==
                                "Second description of second genre.")
        self.assertTrue(correct_descriptions)

    def test_genre_3(self):
        name = "First One"
        description = "Same desc."
        years_on_top = [1000, 2000, 3000]
        artists = ["Artist 1", "Artist 2", "Artist 3"]
        related_genres = ["Some 1", "Some 2", "Some 3"]
        test_genre = Genre(
            name=name, description=description, years_on_top=years_on_top,
            artists=artists, related_genres=related_genres)

        name_2 = "Second One"
        description_2 = "Same desc."
        years_on_top_2 = [1999]
        artists_2 = ["Artist 3", "Artist 4", "Artist 5"]
        related_genres_2 = ["Some 3", "Some 4", "Some 5"]
        test_genre_2 = Genre(
            name=name_2, description=description_2, years_on_top=years_on_top_2,
            artists=artists_2, related_genres=related_genres_2)

        name_3 = "Third One"
        description_3 = "Not same desc."
        years_on_top_3 = [2001, 2005, 2015]
        artists_3 = ["Artist 6", "Artist 7", "Artist 8"]
        related_genres_3 = ["Some 6", "Some 7", "Some 8"]
        test_genre_3 = Genre(
            name=name_3, description=description_3, years_on_top=years_on_top_3,
            artists=artists_3, related_genres=related_genres_3)

        self.session.add_all([test_genre, test_genre_2, test_genre_3])
        self.session.commit()

        genres_list = self.session.query(
            Genre).filter_by(description="Same desc.").all()
        self.assertTrue(len(genres_list) == 2)
        not_genres_list = self.session.query(
            Genre).filter_by(description="Not same desc.").all()
        self.assertTrue(len(not_genres_list) == 1)

if __name__ == '__main__':
    unittest.main()
