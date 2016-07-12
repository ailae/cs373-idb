#!/usr/bin/env python3
"""
Tests.py - Contains unit tests to check the validity of all of our
database's models: Artist, Year, Song, and Genre.
"""

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import BASE, create_all_tables, YearsSongsAssociation, \
    Artist, Year, Song, Genre


class ModelUnitTests(unittest.TestCase):

    """
    ModelUnitTests will create a new database in memory for each
    test and verify that adding entries and querying for them will
    return expected results.
    """

    def setUp(self):
        self.base = BASE
        self.engine = create_engine("sqlite:///:memory:")
        self.made_session = sessionmaker(bind=self.engine)
        self.session = self.made_session()
        create_all_tables(self.engine)

    def tearDown(self):
        self.base.metadata.drop_all(self.engine)

    # These tests ensure that the Artist model behaves as expected.

    def test_artist_1(self):
        artist_id = "abcd"
        name = "Kanye West"
        num_followers = 20000000
        image_url = "www.kanye.com/image.jpg"
        popularity = 50
        test_artist = Artist(
            artist_id=artist_id, name=name, num_followers=num_followers,
            image_url=image_url, popularity=popularity)

        charted_song = Song(song_id="123abc", song_name="Good Life")
        artist_genre_1 = Genre(name="Rap", description="Intense music.")
        test_artist.charted_songs.append(charted_song)

        self.session.add_all([charted_song, artist_genre_1, test_artist])
        self.session.commit()
        self.assertTrue(test_artist in self.session)
        kanye = self.session.query(Artist).filter_by(name="Kanye West").first()
        kanye_image = kanye.image_url
        self.assertEqual(kanye_image, "www.kanye.com/image.jpg")

    def test_artist_2(self):
        artist_id = "abcd"
        name = "Beyonce"
        num_followers = 80000000
        image_url = "https://spotifyinsights.files.wordpress.com/2015/03/" + \
            "beyonce_publicityphoto6-1.jpg"
        popularity = 80
        test_artist = Artist(
            artist_id=artist_id, name=name, num_followers=num_followers,
            image_url=image_url, popularity=popularity)

        charted_song = Song(song_id="456cde", song_name="Flawless")
        artist_genre_1 = Genre(name="R&B", description="Soul music.")
        test_artist.charted_songs.append(charted_song)
        test_artist.genres.append(artist_genre_1)

        self.session.add_all([charted_song, artist_genre_1, test_artist])
        self.session.commit()

        artist_id_2 = "efgh"
        name_2 = "DJ Khaled"
        num_followers_2 = 50
        image_url_2 = "https://i.scdn.co/image/ec4dd6900eb90044"
        popularity_2 = 1
        test_artist_2 = Artist(
            artist_id=artist_id_2, name=name_2, num_followers=num_followers_2,
            image_url=image_url_2, popularity=popularity_2)

        charted_song_2 = Song(song_id="980dj", song_name="Another One")
        artist_genre_2 = Genre(name="Crappy Music", description="Just awful.")
        test_artist_2.charted_songs.append(charted_song_2)
        test_artist_2.genres.append(artist_genre_2)

        self.session.add_all([charted_song_2, artist_genre_2, test_artist_2])
        self.session.commit()

        dj_khaled = self.session.query(
            Artist).filter_by(name="DJ Khaled").first()
        beyonce = self.session.query(Artist).filter_by(name="Beyonce").first()
        random_not_added = self.session.query(
            Artist).filter_by(name="random").first()
        self.assertTrue((dj_khaled is not None) and (
            beyonce is not None) and (random_not_added is None))

    def test_artist_3(self):
        artist_id = "abcd"
        name = "Some Artist"
        num_followers = 123
        image_url = "a_url"
        popularity = 100
        test_artist = Artist(
            artist_id=artist_id, name=name, num_followers=num_followers,
            image_url=image_url, popularity=popularity)

        charted_song = Song(song_id="1234", song_name="First Song")
        charted_songb = Song(song_id="5678", song_name="Another Song")
        artist_genre_1 = Genre(name="Potato", description="Potato music.")
        artist_genre_1b = Genre(name="Tomato", description="Tomato music.")
        test_artist.charted_songs.append(charted_song)
        test_artist.charted_songs.append(charted_songb)
        test_artist.genres.append(artist_genre_1)
        test_artist.genres.append(artist_genre_1b)

        self.session.add_all(
            [charted_song, charted_songb, artist_genre_1,
             artist_genre_1b, test_artist])
        self.session.commit()

        artist_id_2 = "efgh"
        name_2 = "Some Artist 2"
        num_followers_2 = 6589
        image_url_2 = "b_url"
        popularity_2 = 100
        test_artist_2 = Artist(
            artist_id=artist_id_2, name=name_2, num_followers=num_followers_2,
            image_url=image_url_2, popularity=popularity_2)

        charted_song_2 = Song(song_id="8888", song_name="First Song 2")
        charted_song_2b = Song(song_id="9999", song_name="Another Song 2")
        artist_genre_2 = Genre(name="Eggplant", description="Eggplant music.")
        artist_genre_2b = Genre(name="Radish", description="Radish music.")
        test_artist_2.charted_songs.append(charted_song_2)
        test_artist_2.charted_songs.append(charted_song_2b)
        test_artist_2.genres.append(artist_genre_2)
        test_artist_2.genres.append(artist_genre_2b)

        self.session.add_all(
            [charted_song_2, charted_song_2b, artist_genre_2,
             artist_genre_2b, test_artist_2])
        self.session.commit()

        artist_id_3 = "ijkl"
        name_3 = "Some Artist 3"
        num_followers_3 = 20156
        image_url_3 = "c_url"
        popularity_3 = 50
        test_artist_3 = Artist(
            artist_id=artist_id_3, name=name_3, num_followers=num_followers_3,
            image_url=image_url_3, popularity=popularity_3)

        charted_song_3 = Song(song_id="1111", song_name="First Song 3")
        charted_song_3b = Song(song_id="2222", song_name="Another Song 3")
        artist_genre_3 = self.session.query(
            Genre).filter_by(name="Potato").first()
        artist_genre_3b = self.session.query(
            Genre).filter_by(name="Tomato").first()
        test_artist_3.charted_songs.append(charted_song_3)
        test_artist_3.charted_songs.append(charted_song_3b)
        test_artist_3.genres.append(artist_genre_3)
        test_artist_3.genres.append(artist_genre_3b)

        self.session.add_all([charted_song_3, charted_song_3b, test_artist_3])
        self.session.commit()

        hundred_artist_list = self.session.query(
            Artist).filter_by(popularity=100).all()
        self.assertEqual(len(hundred_artist_list), 2)
        self.assertEqual(hundred_artist_list[0].name, "Some Artist")
        self.assertEqual(hundred_artist_list[1].name, "Some Artist 2")

        potato_artist_list = self.session.query(
            Genre).filter_by(name="Potato").first().artists
        self.assertEqual(len(potato_artist_list), 2)
        self.assertTrue(test_artist in potato_artist_list and
                        test_artist_3 in potato_artist_list and
                        test_artist_2 not in potato_artist_list)

        tomato_artist_list = self.session.query(
            Genre).filter_by(name="Tomato").first().artists
        self.assertEqual(len(tomato_artist_list), 2)
        self.assertTrue(test_artist in tomato_artist_list and
                        test_artist_3 in tomato_artist_list and
                        test_artist_2 not in tomato_artist_list)

        eggplant_artist_list = self.session.query(
            Genre).filter_by(name="Eggplant").first().artists
        self.assertEqual(len(eggplant_artist_list), 1)
        self.assertTrue(test_artist not in eggplant_artist_list and
                        test_artist_3 not in eggplant_artist_list and
                        test_artist_2 in eggplant_artist_list)

        radish_artist_list = self.session.query(
            Genre).filter_by(name="Radish").first().artists
        self.assertEqual(len(radish_artist_list), 1)
        self.assertTrue(test_artist not in radish_artist_list and
                        test_artist_3 not in radish_artist_list
                        and test_artist_2 in radish_artist_list)

    # The following tests check the Year model

    def test_year_1(self):
        year = 2001
        top_album_name = "Some Album"
        top_album_id = "1234"
        top_genre_name = "Top Genre Name"
        top_album_artist_id = "artist123"
        top_genre = Genre(name="Top Genre Name", description="Generic genre.")
        self.session.add(top_genre)
        self.session.commit()
        test_year = Year(year=year, top_album_name=top_album_name,
                         top_album_id=top_album_id,
                         top_genre_name=top_genre_name,
                         top_album_artist_id=top_album_artist_id)
        top_song = Song(song_id="same_id", song_name="Some Song")
        top_songb = Song(song_id="other_id", song_name="Other Song")

        test_assoc = YearsSongsAssociation(rank=1)
        test_assoc.song = top_song
        test_year.top_songs.append(test_assoc)

        test_assocb = YearsSongsAssociation(rank=85)
        test_assocb.song = top_songb
        test_year.top_songs.append(test_assocb)
        self.session.add(top_song)
        self.session.add(top_songb)
        self.session.commit()

        self.session.add(test_year)
        self.session.commit()
        self.assertTrue(test_year in self.session)
        actual_year = self.session.query(Year).filter_by(year=2001).first()
        actual_top_genre = actual_year.top_genre
        self.assertEqual("Top Genre Name", actual_top_genre.name)
        self.assertEqual("Generic genre.", actual_top_genre.description)
        self.assertEqual(test_year, actual_top_genre.years_on_top[0])

        all_songs = actual_year.top_songs
        self.assertEqual(len(all_songs), 2)

    def test_year_2(self):
        year = 2015
        top_album_name = "The Biggest Album of 2015"
        top_album_id = "2193810"
        top_genre_name = "Pop"
        top_album_artist_id = "TopAlbumArtist2015"
        top_genre = Genre(name="Pop", description="Pop music.")
        self.session.add(top_genre)
        self.session.commit()
        test_year = Year(year=year, top_album_name=top_album_name,
                         top_album_id=top_album_id,
                         top_genre_name=top_genre_name,
                         top_album_artist_id=top_album_artist_id)
        top_song = Song(song_id="2015A", song_name="The Biggest Song of 2015")
        top_songb = Song(
            song_id="2015B", song_name="The Second Biggest Song of 2015")

        test_assoc = YearsSongsAssociation(rank=1)
        test_assoc.song = top_song
        test_year.top_songs.append(test_assoc)

        test_assocb = YearsSongsAssociation(rank=2)
        test_assocb.song = top_songb
        test_year.top_songs.append(test_assocb)
        self.session.add(top_song)
        self.session.add(top_songb)
        self.session.commit()
        self.session.add(test_year)
        self.session.commit()

        year_2 = 2014
        top_album_name_2 = "The Biggest Album of 2014"
        top_album_id_2 = "999999"
        top_genre_name_2 = "Pop"
        top_album_artist_id_2 = "TopAlbumArtist2014"

        test_year_2 = Year(year=year_2, top_album_name=top_album_name_2,
                           top_album_id=top_album_id_2,
                           top_genre_name=top_genre_name_2,
                           top_album_artist_id=top_album_artist_id_2)
        top_song_2 = Song(
            song_id="2014A", song_name="The Biggest Song of 2014")
        top_song_2b = Song(
            song_id="2014B", song_name="The Second Biggest Song of 2014")

        test_assoc_2 = YearsSongsAssociation(rank=1)
        test_assoc_2.song = top_song_2
        test_year_2.top_songs.append(test_assoc_2)

        test_assoc_2b = YearsSongsAssociation(rank=2)
        test_assoc_2b.song = top_song_2b
        test_year_2.top_songs.append(test_assoc_2b)
        self.session.add(top_song_2)
        self.session.add(top_song_2b)
        self.session.commit()
        self.session.add(test_year_2)
        self.session.commit()

        fifteen = self.session.query(Year).filter_by(year=2015).first()
        fourteen = self.session.query(Year).filter_by(year=2014).first()
        self.assertTrue(fifteen is not None)
        self.assertTrue(fourteen is not None)

        fifteen_top_album = fifteen.top_album_name
        fourteen_top_album = fourteen.top_album_name
        fifteen_top_album_artist = fifteen.top_album_artist_id
        fourteen_top_album_artist = fourteen.top_album_artist_id

        correct_albums = fifteen_top_album == "The Biggest Album of 2015" and \
            fourteen_top_album == "The Biggest Album of 2014"
        self.assertTrue(correct_albums)

        correct_album_artists = fifteen_top_album_artist == \
            "TopAlbumArtist2015" and \
            fourteen_top_album_artist == \
            "TopAlbumArtist2014"
        self.assertTrue(correct_album_artists)

    def test_year_3(self):

        year = 2015
        top_album_name = "The Biggest Album of 2015"
        top_album_id = "2193810"
        top_genre_name = "Rap"
        top_album_artist_id = "TopAlbumArtist2015"
        top_genre = Genre(name="Rap", description="Rap music.")
        self.session.add(top_genre)
        self.session.commit()
        test_year = Year(year=year, top_album_name=top_album_name,
                         top_album_id=top_album_id,
                         top_genre_name=top_genre_name,
                         top_album_artist_id=top_album_artist_id)
        top_song = Song(song_id="2015A", song_name="The Biggest Song of 2015")
        top_songb = Song(
            song_id="2015B", song_name="The Second Biggest Song of 2015")

        test_assoc = YearsSongsAssociation(rank=1)
        test_assoc.song = top_song
        test_year.top_songs.append(test_assoc)

        test_assocb = YearsSongsAssociation(rank=2)
        test_assocb.song = top_songb
        test_year.top_songs.append(test_assocb)
        self.session.add(top_song)
        self.session.add(top_songb)
        self.session.commit()
        self.session.add(test_year)
        self.session.commit()

        year_2 = 2014
        top_album_name_2 = "The Biggest Album of 2014"
        top_album_id_2 = "999999"
        top_genre_name_2 = "Rap"
        top_album_artist_id_2 = "TopAlbumArtist2014"

        test_year_2 = Year(year=year_2, top_album_name=top_album_name_2,
                           top_album_id=top_album_id_2,
                           top_genre_name=top_genre_name_2,
                           top_album_artist_id=top_album_artist_id_2)
        top_song_2 = Song(
            song_id="2014A", song_name="The Biggest Song of 2014")
        top_song_2b = Song(
            song_id="2014B", song_name="The Second Biggest Song of 2014")

        test_assoc_2 = YearsSongsAssociation(rank=1)
        test_assoc_2.song = top_song_2
        test_year_2.top_songs.append(test_assoc_2)

        test_assoc_2b = YearsSongsAssociation(rank=2)
        test_assoc_2b.song = top_song_2b
        test_year_2.top_songs.append(test_assoc_2b)
        self.session.add(top_song_2)
        self.session.add(top_song_2b)
        self.session.commit()
        self.session.add(test_year_2)
        self.session.commit()

        year_3 = 2013
        top_album_name_3 = "The Biggest Album of 2013"
        top_album_id_3 = "3333333333"
        top_genre_name_3 = "Not Rap"
        top_album_artist_id_3 = "TopAlbumArtist2013"
        top_genre = Genre(name="Not Rap", description="Not rap music.")
        self.session.add(top_genre)
        self.session.commit()
        test_year_3 = Year(year=year_3, top_album_name=top_album_name_3,
                           top_album_id=top_album_id_3,
                           top_genre_name=top_genre_name_3,
                           top_album_artist_id=top_album_artist_id_3)
        top_song_3 = Song(
            song_id="2013A", song_name="The Biggest Song of 2013")
        top_song_3b = Song(
            song_id="2013B", song_name="The Second Biggest Song of 2013")

        test_assoc_3 = YearsSongsAssociation(rank=1)
        test_assoc_3.song = top_song_3
        test_year_3.top_songs.append(test_assoc_3)

        test_assoc_3b = YearsSongsAssociation(rank=2)
        test_assoc_3b.song = top_song_2b
        test_year_3.top_songs.append(test_assoc_3b)
        self.session.add(top_song_3)
        self.session.add(top_song_3b)
        self.session.commit()
        self.session.add(test_year_3)
        self.session.commit()

        years_list = self.session.query(
            Year).filter_by(top_genre_name="Rap").all()
        self.assertTrue(len(years_list) == 2)
        self.assertTrue(test_year in years_list and
                        test_year_2 in years_list and
                        test_year_3 not in years_list)

        not_rap_list = self.session.query(
            Year).filter_by(top_genre_name="Not Rap").all()
        self.assertTrue(len(not_rap_list) == 1)
        self.assertTrue(test_year not in not_rap_list and
                        test_year_2 not in not_rap_list and
                        test_year_3 in not_rap_list)
        self.assertEqual(not_rap_list[0], test_year_3)
        self.assertEqual(not_rap_list[0].year, 2013)

    # The following tests will check the Song model

    def test_song_1(self):

        song_id = "99999"
        song_name = "A Song"
        artist_name = "Some Artist"
        artist_id = "1234"
        album_name = "Some Album"
        explicit = True
        popularity = 20

        test_song = Song(
            song_id=song_id, song_name=song_name, artist_name=artist_name,
            artist_id=artist_id, album_name=album_name, explicit=explicit,
            popularity=popularity)

        year_charted_1 = Year(year=1990)
        assoc_1 = YearsSongsAssociation(
            year_num=1990, rank=20, song_id=song_id)
        assoc_1.song = test_song
        assoc_1.year = year_charted_1
        year_charted_1.top_songs.append(assoc_1)
        test_song.years_charted.append(assoc_1)

        self.assertEqual(assoc_1.song_id, test_song.song_id)

        self.session.add_all([year_charted_1, assoc_1, test_song])
        self.session.commit()

        self.assertTrue(test_song in self.session)
        this_song = self.session.query(
            Song).filter_by(song_id="99999").first()

        self.assertTrue(this_song.explicit)
        self.assertEqual(this_song.years_charted[0].year.year, 1990)
        self.assertEqual(year_charted_1.top_songs[0].song.song_name, "A Song")

    def test_song_2(self):

        song_id = "123"
        song_name = "Some Song"
        artist_name = "Some Artist"
        artist_id = "3279"
        album_name = "Some Album"
        explicit = True
        popularity = 10

        test_song = Song(
            song_id=song_id, song_name=song_name, artist_name=artist_name,
            artist_id=artist_id, album_name=album_name, explicit=explicit,
            popularity=popularity)

        song_id_2 = "234"
        song_name_2 = "Second Song"
        artist_name_2 = "Second Artist"
        artist_id_2 = "7890"
        album_name_2 = "Second Album"
        explicit_2 = False
        popularity_2 = 20

        test_song_2 = Song(
            song_id=song_id_2, song_name=song_name_2, artist_name=artist_name_2,
            artist_id=artist_id_2, album_name=album_name_2, explicit=explicit_2,
            popularity=popularity_2)

        self.session.add_all([test_song, test_song_2])
        self.session.commit()

        first_song = self.session.query(Song).filter_by(
            song_id="123").first()
        second_song = self.session.query(Song).filter_by(
            song_id="234").first()
        self.assertTrue(first_song is not None)
        self.assertTrue(second_song is not None)
        correct_explicits = first_song.explicit and not second_song.explicit
        self.assertTrue(correct_explicits)

    def test_song_3(self):

        song_id = "123"
        song_name = "Some Song"
        artist_name = "The Same Artist"
        artist_id = "123121"
        album_name = "The Same Album"
        explicit = True
        popularity = 100

        test_song = Song(
            song_id=song_id, song_name=song_name, artist_name=artist_name,
            artist_id=artist_id, album_name=album_name, explicit=explicit,
            popularity=popularity)

        song_id_2 = "321"
        song_name_2 = "Different Song Same Album"
        artist_name_2 = "The Same Artist"
        artist_id_2 = "123121"
        album_name_2 = "The Same Album"
        explicit_2 = True
        popularity_2 = 99

        test_song_2 = Song(
            song_id=song_id_2, song_name=song_name_2, artist_name=artist_name_2,
            artist_id=artist_id_2, album_name=album_name_2, explicit=explicit_2,
            popularity=popularity_2)

        song_id_3 = "4444"
        song_name_3 = "Different Song Different Album"
        artist_name_3 = "Different Artist"
        artist_id_3 = "00000"
        album_name_3 = "Different Album"
        explicit_3 = False
        popularity_3 = 20

        test_song_3 = Song(
            song_id=song_id_3, song_name=song_name_3, artist_name=artist_name_3,
            artist_id=artist_id_3, album_name=album_name_3, explicit=explicit_3,
            popularity=popularity_3)

        self.session.add_all([test_song, test_song_2, test_song_3])
        self.session.commit()

        same_album_list = self.session.query(Song).filter_by(
            album_name="The Same Album").all()
        self.assertEqual(len(same_album_list), 2)
        self.assertTrue(test_song in same_album_list and
                        test_song_2 in same_album_list
                        and test_song_3 not in same_album_list)

        not_same_album_list = self.session.query(
            Song).filter_by(album_name="Different Album").all()
        self.assertEqual(len(not_same_album_list), 1)
        self.assertTrue(test_song not in not_same_album_list and
                        test_song_2 not in not_same_album_list and
                        test_song_3 in not_same_album_list)

    # The following tests check the Genre model
    def test_genre_1(self):
        name = "The Genre"
        description = "Some description of the genre."
        test_genre = Genre(name=name, description=description)

        artist_1 = Artist(artist_id="FirstArtist", name="The First Artist")
        test_genre.artists.append(artist_1)

        year_1 = Year(year=2015)
        test_genre.years_on_top.append(year_1)

        genre_1 = Genre(name="Related 1", description="Related 1 description")
        test_genre.related_genres.append(genre_1)

        self.session.add_all([artist_1, year_1, genre_1, test_genre])
        self.session.commit()

        self.assertTrue(test_genre in self.session)
        actual_genre = self.session.query(
            Genre).filter_by(name="The Genre").first()

        genre_artists = actual_genre.artists
        self.assertEqual(len(genre_artists), 1)
        self.assertTrue(artist_1 in genre_artists)

        actual_artist = self.session.query(
            Artist).filter_by(name="The First Artist").first()
        artist_genres = actual_artist.genres
        self.assertEqual(len(artist_genres), 1)
        self.assertTrue(test_genre in artist_genres)

        genre_years = actual_genre.years_on_top
        self.assertEqual(len(genre_years), 1)
        self.assertTrue(year_1 in genre_years)

        actual_year = self.session.query(Year).filter_by(year=2015).first()
        year_genre = actual_year.top_genre
        self.assertEqual(test_genre, year_genre)

        genre_relatedgenres = test_genre.related_genres
        self.assertEqual(len(genre_relatedgenres), 1)
        self.assertTrue(genre_1, genre_relatedgenres)

        self.assertTrue(test_genre in self.session)
        actual_genre = self.session.query(
            Genre).filter_by(name="The Genre").first()
        actual_name = actual_genre.name
        self.assertEqual(actual_name, name)

    def test_genre_2(self):
        name = "The Genre"
        description = "Some description of the genre."
        test_genre = Genre(name=name, description=description)

        name_2 = "Second Genre"
        description_2 = "Second description of second genre."
        test_genre_2 = Genre(name=name_2, description=description_2)

        self.session.add_all([test_genre, test_genre_2])
        self.session.commit()

        first_genre = self.session.query(
            Genre).filter_by(name="The Genre").first()
        second_genre = self.session.query(
            Genre).filter_by(name="Second Genre").first()
        self.assertTrue(first_genre is not None)
        self.assertTrue(second_genre is not None)
        correct_descriptions = (first_genre.description ==
                                "Some description of the genre.") and \
                               (second_genre.description ==
                                "Second description of second genre.")
        self.assertTrue(correct_descriptions)

    def test_genre_3(self):
        name = "First One"
        description = "Same desc."
        test_genre = Genre(name=name, description=description)

        name_2 = "Second One"
        description_2 = "Same desc."
        test_genre_2 = Genre(name=name_2, description=description_2)

        name_3 = "Third One"
        description_3 = "Not same desc."
        test_genre_3 = Genre(name=name_3, description=description_3)

        # Make Test Genre 1 and 2 related
        test_genre.related_genres.append(test_genre_2)
        test_genre_2.related_genres.append(test_genre)

        # Make Test Genre 1 and 3 related
        test_genre.related_genres.append(test_genre_3)
        test_genre_3.related_genres.append(test_genre)

        artist_1 = Artist(artist_id="Common Artist 1234")

        # Add genres to the artist, but don't directly add the artist
        # to the genres. This will allow us to check whether back-population
        # is occurring.
        artist_1.genres.append(test_genre)
        artist_1.genres.append(test_genre_3)

        self.session.add_all(
            [artist_1, test_genre, test_genre_2, test_genre_3])
        self.session.commit()

        genres_list = self.session.query(
            Genre).filter_by(description="Same desc.").all()
        self.assertTrue(len(genres_list) == 2)
        not_genres_list = self.session.query(
            Genre).filter_by(description="Not same desc.").all()
        self.assertTrue(len(not_genres_list) == 1)

        actual_genre_1 = self.session.query(
            Genre).filter_by(name="First One").first()
        self.assertTrue(actual_genre_1 is not None)
        actual_genre_2 = self.session.query(
            Genre).filter_by(name="Second One").first()
        self.assertTrue(actual_genre_2 is not None)
        actual_genre_3 = self.session.query(
            Genre).filter_by(name="Third One").first()
        self.assertTrue(actual_genre_3 is not None)
        actual_artist = self.session.query(Artist).filter_by(
            artist_id="Common Artist 1234").first()
        self.assertTrue(actual_artist is not None)

        first_relateds = actual_genre_1.related_genres
        self.assertTrue(
            actual_genre_2 in first_relateds and
            actual_genre_3 in first_relateds)

        second_relateds = actual_genre_2.related_genres
        self.assertTrue(actual_genre_1 in second_relateds)

        third_relateds = actual_genre_3.related_genres
        self.assertTrue(actual_genre_1 in third_relateds)

        # Artist-related. Ensure back-population is occuring from artists to
        # genres.
        self.assertTrue(actual_genre_1 in actual_artist.genres
                        and actual_genre_3 in actual_artist.genres)
        self.assertTrue(actual_artist in actual_genre_1.artists)
        self.assertTrue(actual_artist in actual_genre_3.artists)

    # The following tests evaluate the dictify method on each of the models.
    def test_dictify_artist(self):
        expected = {
            'artist_id': 'abcd',
            'name': 'Drake',
            'num_followers': 12345,
            'image_url': "www.drake.com",
            'popularity': 100,
            'charted_songs': ['One Dance', 'Take Care'],
            'genres': ['Rap', 'Hip-Hop']
        }

        drake = Artist(artist_id="abcd", name="Drake", num_followers=12345,
                       image_url="www.drake.com", popularity=100)
        one_dance = Song(song_name="One Dance", song_id="od")
        take_care = Song(song_name="Take Care", song_id="tc")

        rap = Genre(name="Rap", description="Rap music.")
        hip_hop = Genre(name="Hip-Hop", description="Hip hop music.")

        drake.charted_songs.append(one_dance)
        drake.charted_songs.append(take_care)

        drake.genres.append(rap)
        drake.genres.append(hip_hop)

        self.session.add_all([drake, one_dance, take_care, rap, hip_hop])
        self.session.commit()

        returned_drake = self.session.query(
            Artist).filter_by(name="Drake").first()

        actual_dict = returned_drake.dictify()

        # The lists in the dictionary can be in any order, so
        # we have to compare the values line by line or it will fail.
        self.assertEqual(expected['artist_id'], actual_dict['artist_id'])
        self.assertEqual(expected['name'], actual_dict['name'])
        self.assertEqual(expected['num_followers'],
                         actual_dict['num_followers'])
        self.assertEqual(expected['image_url'], actual_dict['image_url'])
        self.assertEqual(expected['popularity'], actual_dict['popularity'])

        self.assertEqual(len(actual_dict['genres']), 2)
        self.assertTrue("Rap" in actual_dict['genres'])
        self.assertTrue("Hip-Hop" in actual_dict['genres'])
        self.assertEqual(len(actual_dict['charted_songs']), 2)
        self.assertTrue("One Dance" in actual_dict['charted_songs'])
        self.assertTrue("Take Care" in actual_dict['charted_songs'])

    def test_dictify_genre(self):
        expected = {
            'name': 'Dance',
            'description': "Dance music.",
            'years_on_top': [],
            'artists': ['Ke$ha', 'Dancer 1'],
            'related_genres': ['Trance']
        }

        dance = Genre(name='Dance', description='Dance music.')
        kesha = Artist(artist_id='abcd', name='Ke$ha')
        dancer1 = Artist(artist_id='defg', name='Dancer 1')
        trance = Genre(name='Trance', description='Trance music.')

        dance.artists.append(kesha)
        dance.artists.append(dancer1)

        dance.related_genres.append(trance)

        self.session.add_all([dance, kesha, dancer1, trance])
        self.session.commit()

        returned_dance = self.session.query(Genre) \
            .filter_by(name="Dance").first()
        actual_dict = returned_dance.dictify()
        self.assertEqual(expected['name'], actual_dict['name'])
        self.assertEqual(expected['description'], actual_dict['description'])
        self.assertEqual(expected['years_on_top'],
                         actual_dict['years_on_top'])

        self.assertEqual(len(actual_dict['artists']), 2)
        self.assertTrue("Ke$ha" in actual_dict['artists'])
        self.assertTrue("Dancer 1" in actual_dict['artists'])
        self.assertEqual(len(actual_dict['related_genres']), 1)
        self.assertTrue("Trance" in actual_dict['related_genres'])

    def test_dictify_song(self):
        expected = {
            'song_id': 'abcd',
            'song_name': 'A Song Name',
            'artist_name': 'Artist Name',
            'artist_id': 'efgh',
            'album_name': 'The Album Name',
            'explicit': True,
            'popularity': 20,
            'years_charted': [1990, 1991, 1992, 2015]
        }

        some_song = Song(song_id="abcd", song_name="A Song Name",
                         artist_name="Artist Name", artist_id="efgh",
                         album_name="The Album Name", explicit=True,
                         popularity=20)

        artist = Artist(name="Artist Name", artist_id="efgh")

        year1 = Year(year=1990)
        year2 = Year(year=1991)
        year3 = Year(year=1992)
        year4 = Year(year=2015)

        assoc_y1 = YearsSongsAssociation(year_num=1990, rank=1,
                                         song_id="abcd")
        assoc_y1.year = year1
        assoc_y2 = YearsSongsAssociation(year_num=1991, rank=1,
                                         song_id="abcd")
        assoc_y2.year = year2
        assoc_y3 = YearsSongsAssociation(year_num=1992, rank=1,
                                         song_id="abcd")
        assoc_y3.year = year3

        assoc_y4 = YearsSongsAssociation(year_num=2015, rank=1,
                                         song_id="abcd")
        assoc_y4.year = year4

        some_song.years_charted.append(assoc_y1)
        some_song.years_charted.append(assoc_y2)
        some_song.years_charted.append(assoc_y3)
        some_song.years_charted.append(assoc_y4)

        self.session.add_all([some_song, artist, year1, year2, year3, year4,
                              assoc_y1, assoc_y2, assoc_y3, assoc_y4])
        self.session.commit()

        returned_song = self.session.query(Song) \
            .filter_by(song_name="A Song Name").first()

        actual_dict = returned_song.dictify()

        self.assertEqual(actual_dict['song_id'], expected['song_id'])
        self.assertEqual(actual_dict['song_name'], expected['song_name'])
        self.assertEqual(actual_dict['artist_name'], expected['artist_name'])
        self.assertEqual(actual_dict['artist_id'], expected['artist_id'])
        self.assertEqual(actual_dict['album_name'], expected['album_name'])
        self.assertEqual(actual_dict['explicit'], expected['explicit'])
        self.assertEqual(actual_dict['popularity'], expected['popularity'])

        self.assertTrue(1990 in actual_dict['years_charted'])
        self.assertTrue(1991 in actual_dict['years_charted'])
        self.assertTrue(1992 in actual_dict['years_charted'])
        self.assertTrue(2015 in actual_dict['years_charted'])

    def test_dictify_year(self):
        expected = {
            'year': 2000,
            'top_album_name': 'Top Album',
            'top_album_id': 'tgvjs',
            'top_genre_name': 'Top Genre',
            'top_album_artist_id': 'sadsd',
            'top_songs': ['Top Song 1', 'Top Song 2']
        }

        year = Year(year=2000, top_album_name='Top Album',
                    top_album_id='tgvjs', top_genre_name='Top Genre',
                    top_album_artist_id='sadsd')

        song1 = Song(song_id='abcd', song_name='Top Song 1')
        assoc_s1 = YearsSongsAssociation(year_num=2000, rank=2,
                                         song_id="abcd")
        assoc_s1.song = song1
        song2 = Song(song_id='efgh', song_name='Top Song 2')
        assoc_s2 = YearsSongsAssociation(year_num=2000, rank=1,
                                         song_id="efgh")
        assoc_s2.song = song2

        year.top_songs.append(assoc_s1)
        year.top_songs.append(assoc_s2)

        self.session.add_all([year, song1, song2, assoc_s1, assoc_s2])
        self.session.commit()

        returned_year = self.session.query(Year) \
            .filter_by(year=2000).first()

        actual_dict = returned_year.dictify()

        self.assertEqual(actual_dict['year'], expected['year'])
        self.assertEqual(
            actual_dict['top_album_name'], expected['top_album_name'])
        self.assertEqual(actual_dict['top_album_id'], expected['top_album_id'])
        self.assertEqual(
            actual_dict['top_genre_name'], expected['top_genre_name'])
        self.assertEqual(
            actual_dict['top_album_artist_id'], expected['top_album_artist_id'])

        self.assertTrue('Top Song 1' in actual_dict['top_songs'])
        self.assertTrue('Top Song 2' in actual_dict['top_songs'])


if __name__ == '__main__':
    unittest.main()
