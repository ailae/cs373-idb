#!/usr/bin/env python3


from unittest import main, TestCase
import models


class ModelUnitTests(TestCase):

	def setUp(self):
		db.create_all()

	def artist_model_test_1(self):
		name = "Kanye West"
		image_url = "http://cdn.uinterview.com/wp-content/uploads/2016/02/news-kanye-west.jpg"
		image = Image(500, image_url, 500)
		genres = ["Rap", "Hip Hop"]
		popularity = 50
		top_tracks = ["Blood On The Leaves", "Saint Pablo"]
		test_artist = Artist(name, image, genres, popularity, top_tracks, spotify_url)
		db.session.add(test_artist)
		db.session.commit()
		db_artists = Artist.query.all()
		print(db_artists)

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