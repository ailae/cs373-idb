#!/usr/bin/env python3

from flask import Flask
from flask_testing import TestCase
from unittest import main
import models

# Lot of guidance on testing format obtained from
# http://flask-sqlalchemy.pocoo.org/2.1/queries/

class ModelUnitTests(TestCase):

	def create_app(self):
			app = Flask(__name__)
			app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
			app.config['TESTING'] = True
			return app

	def setUp(self):
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()


	# These tests ensure that the Artist model behaves as expected.

	# Tests that once the instance is added to the database, it is found
	# and checks that one of its attributes returns the specified value.
	def test_artist_1(self):
		name = "Kanye West"
		image_url = "http://cdn.uinterview.com/wp-content/uploads/2016/02/news-kanye-west.jpg"
		image_height = 34
		image_width = 54
		genres = ["Rap", "Hip Hop"]
		popularity = 50
		top_songs = ["Blood On The Leaves", "Saint Pablo"]
		spotify_url = "http://www.spotify.com/kanye"
		test_artist = Artist(name, image_height, image_width, image_url, 
							genres, spotify_url, top_songs, popularity)
		db.session.add(test_artist)
		db.session.commit()
		assertTrue(test_artist in db.session)
		kanye = Artist.query.filter_by(name="Kanye West").first()
		kanye_image = kanye.image_url
		assertEquals(kanye_image, image_url)

	# Add two artists, and ensure they are in the database. Search for an artist that 
	# wasn't added, and ensure that it is not found in the database.
	def test_artist_2(self):
		name = "Beyonce"
		image_url = "https://spotifyinsights.files.wordpress.com/2015/03/beyonce_publicityphoto6-1.jpg"
		image_height = 300
		image_width = 593
		genres = ["R&B", "Pop"]
		popularity = 80
		top_songs = ["Drunk In Love"]
		spotify_url = "http://www.spotify.com/beyonce"
		test_artist = Artist(name, image_height, image_width, image_url, genres, spotify_url, top_songs, popularity)
		name_2 = "DJ Khaled"
		image_url_2 = "https://i.scdn.co/image/ec4dd6900eb90044"
		image_height_2 = 200
		image_width_2 = 200
		genres_2 = ["R&B", "Hip Hop", "Rap"]
		popularity_2 = 21
		top_songs_2 = ["Hold You Down"]
		spotify_url_2 = "http://www.spotify.com/djkhaled"
		test_artist_2 = Artist(name_2, image_height_2, image_width_2, image_url_2, genres_2, spotify_url_2, top_songs_2, popularity_2)
		
		db.session.add(test_artist)
		db.session.add(test_artist_2)
		db.session.commit()

		dj_khaled = Artist.query.filter_by(name="DJ Khaled").first()
		beyonce = Artist.query.filter_by(name="Beyonce").first()
		random_not_added = Artist.query.filter_by(name="random").first()
		assertTrue((dj_khaled is not None) and (beyonce is not None) and (random_not_added is None))

	# Add two artists to the database, then filter them by an attribute whose
	# value they have in common. A third artist is added as well, who doesn't share
	# the same value. Ensure that the returned filter list only has two artists.
	def test_artist_3(self):
		name = "SomeArtist"
		image_url = "some_url"
		image_height = 5000
		image_width = 5000
		genres = ["Potato", "Tomato"]
		popularity = 100
		top_songs = ["First Song", "Another Song"]
		spotify_url = "http://www.spotify.com/artist"
		test_artist = Artist(name, image_height, image_width, image_url, genres, spotify_url, top_songs, popularity)
		db.session.add(test_artist)
		db.session.commit()

		name = "AnotherArtist"
		image_url = "some_url"
		image_height = 5000
		image_width = 5000
		genres = ["Potato", "Tomato"]
		popularity = 100
		top_songs = ["First Song", "Another Song"]
		spotify_url = "http://www.spotify.com/artist"
		test_artist_2 = Artist(name, image_height, image_width, image_url, genres, spotify_url, top_songs, popularity)
		db.session.add(test_artist_2)
		db.session.commit()

		name = "Some random artist"
		image_url = "some_url"
		image_height = 5000
		image_width = 5000
		genres = ["Potato", "Tomato"]
		popularity = 2
		top_songs = ["First Song", "Another Song"]
		spotify_url = "http://www.spotify.com/artist"
		test_artist_3 = Artist(name, image_height, image_width, image_url, genres, spotify_url, top_songs, popularity)
		db.session.add(test_artist_3)
		db.session.commit()

		artist_list = Artist.query.filter_by(popularity=100).all()
		assertTrue(len(artist_list) == 2)

	# The following tests check the Year model

	# Add a year to the database, verify that it can be found, 
	# retrieve the top_genre from that year, and verify it matches
	# what is expected.
	def test_year_1(self):
		year = 2001
		top_songs = ["Some Really Popular Song", "Some Other Song"]
		top_genre = "Dubstep"
		top_artist = "NSYNC"
		top_album = "The Best Album"
		test_year = Year(year, top_songs, top_genre, top_artist, top_album)
		db.session.add(test_year)
		db.session.commit()

		assertTrue(test_year in db.session)
		actual_year = Year.query.filter_by(year=2001).first()
		actual_top_genre = actual_year.top_genre
		assertEquals(top_genre, actual_top_genre)

	def test_year_2(self):
		year = 2015
		top_songs = ["New Song", "Old Song"]
		top_genre = "Pop"
		top_artist = "Some Important Artist"
		top_album = "The Biggest Album of 2015"
		test_year = Year(year, top_songs, top_genre, top_artist, top_album)
		year_2 = 2014
		top_songs_2 = ["Another New Song", "Older Song"]
		top_genre_2 = "Rap"
		top_artist_2 = "Rapper"
		top_album_2 = "The Biggest Album of 2014"
		test_year_2 = Year(year_2, top_songs_2, top_genre_2, top_artist_2, top_album_2)
		db.session.add(test_year)
		db.session.add(test_year_2)
		db.session.commit()

		fifteen = Year.query.filter_by(year=2015).first()
		fourteen = Year.query.filter_by(year=2014).first()
		assertTrue(fifteen is not None)
		assertTrue(fourteen is not None)
		fifteen_top_album = fifteen.top_album
		fourteen_top_album = fourteen.top_album
		correct_albums = fifteen_top_album == top_album and 
					   fourteen_top_album == top_album_2
		assertTrue(correct_albums) 

	def test_year_3(self):
		year = 2015
		top_songs = ["New Song", "Old Song"]
		top_genre = "Rap"
		top_artist = "Some Important Artist"
		top_album = "The Biggest Album of 2015"
		test_year = Year(year, top_songs, top_genre, top_artist, top_album)
		year_2 = 2014
		top_songs_2 = ["Another New Song", "Older Song"]
		top_genre_2 = "Rap"
		top_artist_2 = "Rapper"
		top_album_2 = "The Biggest Album of 2014"
		test_year_2 = Year(year, top_songs, top_genre, top_artist, top_album)
		year_3 = 2013
		top_songs_3 = ["thirteen", "another thirteen"]
		top_genre_3 = "Pop"
		top_artist_3 = "Some dude"
		top_album_3 = "The Biggest Album of 2013"
		test_year_3 = Year(year, top_songs, top_genre, top_artist, top_album)
		db.session.add(test_year)
		db.session.add(test_year_2)
		db.session.add(test_year_3)
		db.session.commit()

		# If we search for years who only had a top genre of rap, we should
		# only get two years, not three.
		years_list = Year.query.filter_by(top_genre="Rap").all()
		assertTrue(len(years_list) == 2)

	# The following tests will check the Song model

	def test_song_1(self):
		name = "A Song"
		artist = "Some Artist"
		album = "Some Album"
		explicit = True
		popularity = 10
		spotify_url = "www.spotify.com/some_url"
		test_song = Song(name, artist, album, explicit, popularity, spotify_url)

		db.session.add(test_song)
		db.session.commit()

		assertTrue(test_song in db.session)
		this_song = Song.query.filter(name="A Song")
		this_song_explicit = this_song.explicit
		assertTrue(this_song_explicit)

	def test_song_2(self):
		name = "Some Song"
		artist = "Some Artist"
		album = "Some Album"
		explicit = True
		popularity = 10
		spotify_url = "www.spotify.com/some_url"
		test_song = Song(name, artist, album, explicit, popularity, spotify_url)

		db.session.add(test_song)
		db.session.commit()

		name = "Second Song"
		artist = "Second Artist"
		album = "Second Album"
		explicit = False
		popularity = 20
		spotify_url = "www.spotify.com/some_other_url"
		test_song_2 = Song(name, artist, album, explicit, popularity, spotify_url)

		db.session.add(test_song_2)
		db.session.commit()

		first_song = Song.query.filter_by(name="Some Song").first()
		second_song = Song.query.filter_by(name="Second Song").first()
		assertTrue(first_song is not None)
		assertTrue(second_song is not None)
		correct_explicits = (first_song.explicit == True) and
							(second_song.explicit == False)
		assertTrue(correct_explicits)

	def test_song_3(self):
		name = "Some Song"
		artist = "The Same Artist"
		album = "The Same Album"
		explicit = True
		popularity = 100
		spotify_url = "www.spotify.com/some_url"
		test_song = Song(name, artist, album, explicit, popularity, spotify_url)

		db.session.add(test_song)
		db.session.commit()

		name = "Different Song Same Album"
		artist = "The Same Artist"
		album = "The Same Album"
		explicit = True
		popularity = 99
		spotify_url = "www.spotify.com/some_url_of_diff_song"
		test_song_2 = Song(name, artist, album, explicit, popularity, spotify_url)

		db.session.add(test_song_2)
		db.session.commit()

		name = "Different Song Diff Album"
		artist = "Diff Artist"
		album = "Diff Album"
		explicit = False
		popularity = 20
		spotify_url = "www.spotify.com/totally_diff"
		test_song_3 = Song(name, artist, album, explicit, popularity, spotify_url)

		db.session.add(test_song_3)
		db.session.commit()

		songs_list = Song.query.filter_by(album="The Same Album").all()
		assertTrue(len(songs_list) == 2)
		not_songs_list = Song.query.filter_by(explicit=False).all()
		assertTrue(len(not_songs_list) == 1)

	# The following tests check the Genre model
	def test_genre_1(self):
		name = "The Genre"
		description = "Some description of the genre."
		years_on_top = [2001, 2002, 2003]
		artists = ["Artist 1", "Artist 2", "Artist 3"]
		related_genres = ["Related 1", "Related 2", "Related 3"]
		test_genre = Genre(name, description, years_on_top, artists, related_genres)

		db.session.add(test_genre)
		db.session.commit()

		assertTrue(test_genre in db.session)
		actual_genre = Genre.query.filter_by(name="The Genre").first()
		actual_name = actual_genre.name
		assertEquals(actual_name, name)

	def test_genre_2(self):
		name = "The Genre"
		description = "Some description of the genre."
		years_on_top = [2001, 2002, 2003]
		artists = ["Artist 1", "Artist 2", "Artist 3"]
		related_genres = ["Related 1", "Related 2", "Related 3"]
		test_genre = Genre(name, description, years_on_top, artists, related_genres)

		db.session.add(test_genre)
		db.session.commit()

		name = "Second Genre"
		description = "Second description of second genre."
		years_on_top = [1999]
		artists = ["Artist 1", "Artist 41", "Artist 34"]
		related_genres = ["Related 18732", "Related 2", "Related 3242"]
		test_genre_2 = Genre(name, description, years_on_top, artists, related_genres)

		db.session.add(test_genre_2)
		db.session.commit()

		first_genre = Genre.query.filter_by(name="The Genre").first()
		second_genre = Genre.query.filter_by(name="Second Genre").first()
		assertTrue(first_genre is not None)
		assertTrue(second_genre is not None)
		correct_descriptions = (first_genre.description == 
								"Some description of second genre.") and
								(second_genre.description == 
								"Second description of second genre.")
		assertTrue(correct_descriptions)

	def test_genre_3(self):
		name = "First One"
		description = "Same desc."
		years_on_top = [1000, 2000, 3000]
		artists = ["Artist 1", "Artist 2", "Artist 3"]
		related_genres = ["Some 1", "Some 2", "Some 3"]
		test_genre = Genre(name, description, years_on_top, artists, related_genres)

		db.session.add(test_genre)
		db.session.commit()

		name = "Second One"
		description = "Same desc."
		years_on_top = [1999]
		artists = ["Artist 3", "Artist 4", "Artist 5"]
		related_genres = ["Some 3", "Some 4", "Some 5"]
		test_genre_2 = Genre(name, description, years_on_top, artists, related_genres)

		db.session.add(test_genre_2)
		db.session.commit()

		name = "Third One"
		description = "Not same desc."
		years_on_top = [2001, 2005, 2015]
		artists = ["Artist 6", "Artist 7", "Artist 8"]
		related_genres = ["Some 6", "Some 7", "Some 8"]
		test_genre_3 = Genre(name, description, years_on_top, artists, related_genres)

		db.session.add(test_genre_3)
		db.session.commit()

		genres_list = Genre.query.filter_by(description="Same desc.").all()
		assertTrue(len(genres_list) == 2)
		not_genres_list = Genre.query.filter_by(description="Not same desc.").all()
		assertTrue(len(not_genres_list) == 1)

if __name__ == '__main__':
	unittest.main()

#http://flask-sqlalchemy.pocoo.org/2.1/quickstart/

	# def artist_model_test_1(self):
	# 	name = "Kanye West"
	# 	image_url = "http://cdn.uinterview.com/wp-content/uploads/2016/02/news-kanye-west.jpg"
	# 	image = Image(500, image_url, 500)
	# 	genres = ["Rap", "Hip Hop"]
	# 	popularity = 50
	# 	top_tracks = ["Blood On The Leaves", "Saint Pablo"]
	# 	test_artist = Artist(name, image, genres, popularity, top_tracks, spotify_url)
 #        expect = "Artist(name=%r, image=%r, genre=%r, popularity=%r, topTracks=%r, spotifyUrl=%r)" % (
 #                    name,
 #                    image,
 #                    genres,
 #                    popularity,
 #                    top_tracks,
 #               		spotify_url  
 #                )
	# 	assertEquals(expect, test_artist.__repr__())