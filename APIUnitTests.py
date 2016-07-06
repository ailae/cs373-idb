#!/usr/bin/env python3

# Tests for Sweetify's API

from  unittest import Main, TestCase
import requests
import json

class APIUnitTests(TestCase):

	def setUp(self):
		self.base_api_url = "http://sweetify.me"
	
	def years_get_test_1(self):
		final_url = self.base_api_url + "/years/2000"
		data = "some data"
		received_response = requests.get(final_url, data=data)
		# If received response is not 200, throw an assertion.
		assertTrue(received_response.ok)
		response_dict = json.loads(received_response.content)
		expect_top_song = "Breathe"
		actual_top_song = response_dict.get("top_song")
		assertEquals(actual_top_song, expect_top_song)

	def years_get_test_2(self):
		final_url = self.base_api_url + "/years/2000"
		data = "some data"
		received_response = requests.get(final_url, data=data)
		# If received response is not 200, throw an assertion.
		assertTrue(received_response.ok)
		response_dict = json.loads(received_response.content)
		expect_top_album = "No Strings Attached"
		actual_top_album = response_dict.get("top_album")
		assertEquals(actual_top_album, expect_top_album)

	def years_get_test_3(self):
		final_url = self.base_api_url + "/years/2000"
		data = "some data"
		received_response = requests.get(final_url, data=data)
		# If received response is not 200, throw an assertion.
		assertTrue(received_response.ok)
		response_dict = json.loads(received_response.content)
		expect_top_song_genre = "Country"
		actual_top_song_genre = response_dict.get("top_song_genre")
		assertEquals(actual_top_song_genre, expected_top_song_genre)

	def years_get_test_4(self):
		final_url = self.base_api_url + "/years/2000"
		data = "some data"
		received_response = requests.get(final_url, data=data)
		# If received response is not 200, throw an assertion.
		assertTrue(received_response.ok)
		response_dict = json.loads(received_response.content)
		expect_year = "2000"
		actual_year = response_dict.get("year")
		assertEquals(actual_year, expect_year)

	def years_get_test_5(self):
		final_url = self.base_api_url + "/years/2000"
		data = "some data"
		received_response = requests.get(final_url, data=data)
		# If received response is not 200, throw an assertion.
		assertTrue(received_response.ok)
		response_dict = json.loads(received_response.content)
		expect_top_artist = "Faith Hill"
		actual_top_artist = response_dict.get("top_artist")
		assertEquals(actual_top_artist, expect_top_artist)

	# Test artists

	def artists_get_test_1(self):
		final_url = self.base_api_url + "/artists/drake"
		data = "some data"
		received_response = requests.get(final_url, data=data)
		# If received response is not 200, throw an assertion.
		assertTrue(received_response.ok)
		response_dict = json.loads(received_response.content)
		expect_top_song = ""
		actual_top_song = response_dict.get("top_song")
		assertEquals(actual_top_song, expect_top_song)

	def artists_get_test_2(self):
		final_url = self.base_api_url + "/artists/drake"
		data = "some data"
		received_response = requests.get(final_url, data=data)
		# If received response is not 200, throw an assertion.
		assertTrue(received_response.ok)
		response_dict = json.loads(received_response.content)
		expect_top_album = ""
		actual_top_album = response_dict.get("top_album")
		assertEquals(actual_top_album, expect_top_album)

	def artists_get_test_3(self):
		final_url = self.base_api_url + "/artists/drake"
		data = "some data"
		received_response = requests.get(final_url, data=data)
		# If received response is not 200, throw an assertion.
		assertTrue(received_response.ok)
		response_dict = json.loads(received_response.content)
		expect_top_song_genre = ""
		actual_top_song_genre = response_dict.get("top_song_genre")
		assertEquals(actual_top_song_genre, expected_top_song_genre)

	def artists_get_test_4(self):
		final_url = self.base_api_url + "/artists/drake"
		data = "some data"
		received_response = requests.get(final_url, data=data)
		# If received response is not 200, throw an assertion.
		assertTrue(received_response.ok)
		response_dict = json.loads(received_response.content)
		expect_year = ""
		actual_year = response_dict.get("year")
		assertEquals(actual_year, expect_year)

	def artists_get_test_5(self):
		final_url = self.base_api_url + "/artists/drake"
		data = "some data"
		received_response = requests.get(final_url, data=data)
		# If received response is not 200, throw an assertion.
		assertTrue(received_response.ok)
		response_dict = json.loads(received_response.content)
		expect_top_artist = "Faith Hill"
		actual_top_artist = response_dict.get("top_artist")
		assertEquals(actual_top_artist, expect_top_artist)