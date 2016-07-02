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

	def test_artist_1(self):
		name = "Kanye West"
		image_url = "http://cdn.uinterview.com/wp-content/uploads/2016/02/news-kanye-west.jpg"
		image_height = 34
		image_width = 54
		genres = ["Rap", "Hip Hop"]
		popularity = 50
		top_songs = ["Blood On The Leaves", "Saint Pablo"]
		spotify_url = "http://www.spotify.com/kanye"
		test_artist = Artist(name, image_height, image_width, image_url, genres, spotify_url, top_songs, popularity)
		db.session.add(test_artist)
		db.session.commit()
		assertTrue(test_artist in db.session)
		kanye = Artist.query.filter_by(name="Kanye West").first()
		kanye_image = kanye.image_url
		assertEquals(kanye_image, image_url)

	# Add two artists, ensure that they are found by queries
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
	# value they have in common. Ensure that the returned list contains two of them.
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
		artist_list = Artist.query.filter(popularity=100).all()
		assertTrue(len(artist_list) == 2)


			

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