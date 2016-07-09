from flask import Flask, render_template
from models import *
from sqlalchemy.orm import sessionmaker
import ast

def artists_and_songs(session):
	json = open('JSON/songs.txt', 'r').read()
	songs = ast.literal_eval(json)
	json2 = open('JSON/artists.txt', 'r').read()
	artists = ast.literal_eval(json2)

	try:
		for a in artists:
			artist = Artist(name=a['name'], num_followers=a['num_followers'], 
			artist_id=a['artist_id'], image_url=a['image_url'], 
			popularity=a['popularity'])
			session.add(artist)
			session.commit()

		# Now, make an association between the artist and their genres.
		# artist_genres = a['genres']
		# for a_genre in artist_genres:
		# 	genre_to_add = session.query(Genre).filter_by(name=a_genre).first()
		# 	artist.genres.append(genre_to_add)

		for s in songs:  
			test_song = session.query(Song).filter_by(song_id=s['song_id']).first()
			if not test_song:
				song = Song(song_id = s['song_id'], song_name = s['song_name'],
					artist_id = s['artist_id'], artist_name = s['artist_name'], 
					album_name = s['album_name'], explicit = s['explicit'], 
					popularity = s['popularity'])
				session.add(song)
				session.commit()

		# Make the charted_songs and artist relationship
		for a in session.query(Artist).all():
			for s in session.query(Song).filter_by(artist_id = a.artist_id).all():
				a.charted_songs.append(s)
				# print a.artist_id
				# print s.artist.artist_id
				# s.artist = a

	except:
		session.rollback()
		raise

app = Flask(__name__)
engine = db_connect()
create_all_tables(engine)
session_maker = sessionmaker(bind=engine)
session = session_maker()
# artists_and_songs(session)

#json3 = open('JSON/years.txt', 'r').read()
#years = ast.literal_eval(json3)
#json4 = open('JSON/genres.txt', 'r').read()
#genres = ast.literal.eval(json4)
# Note: genres should contain all genres, meaning the genres of each artist
# AND the genre of all #1 songs of each year.

	# try:
	# 	for g in genres:
	# 		genre = Genre(name=g['name'], description=g['description'])
	# 		session.add(genre)
	# 	# Commit after adding genres so we can query for them later.
	# 	session.commit()
	# except:
	# 	session.rollback()
	# 	raise

	# try:
	# 	# Now that we have added all of our genres, we make associations 
	# 	# between related genres.
	# 	for g in genres:
	# 		this_genre = session.query(Genre).filter_by(name=g['name']).first()
	# 		related_genres = g['related_genres']
	# 		for related_genre in related_genres:
	# 			# Get the object of the related genre.
	# 			rg_object = session.query(Genre).filter_by(name=related_genre)
	# 			# Append that genre to this genre's related genres column.
	# 			this_genre.related_genres.append(rg_object)
	# 	session.commit()
	# except:
	# 	session.rollback()
	# 	raise

	# try:
	# 	for y in years:
	# 		year = Year(year=y['year'], top_album_name=y['top_album_name'], 
	# 					top_album_id=y['top_album_id'], top_genre_name=y['top_genre_name'],
	# 					top_album_artist_id=y['top_album_artist_id'])

			
	# 		# Now we will add this year to the its top genre's years_on_top column.
	# 		# This code assumes the top genre for each year was also added to the
	# 		# genres file--therefore it thinks all genres exist in the database at this
	# 		# point, so it can query for them.
	# 		top_genre_object = session.query(Genre).filter_by(name=y['top_genre_name'])
	# 		top_genre_object.years_on_top.append(year)
	# 		session.add(year)
	# 	session.commit()
	# except:
	# 	session.rollback()
	# 	raise

	## Once all songs and years have been added, it's time to add the top songs to each year
		# make a file that looks just like merged_charts.txt but has removed all of the
		# songs that we didn't add to our database...and has each song's id

		# for each year:
			# for each song in the current_year:
				# current_song_object = session.query(Song).filter_by(song_id=current_song_id).first()
				# current_year.top_songs.append(current_song_object)

		# The above code will append the song object to the year's top songs, and then 
		# by association add that year to the song's years_charted column




	#artist = Artist(**TEST_DATA)
	#artist2 = Artist(name='Drake', num_followers=123, artist_id='abcd', image_url='http://www.google.com', popularity=72, spotify_url='http://www.spotify.com')
	#session.add(artist)
	#session.delete(artist2)
	#session.query(Artist).filter(Artist.name=="Drake").delete()
	# session.commit()

@app.route('/')
def homepage():
	return render_template('index.html')
@app.route('/about')
def about():
	return render_template('about.html')
@app.route('/years')
def years():
	return render_template('years.html')
@app.route('/songs')
def songs():
	song = session.query(Song).all()
	return render_template('songs.html', songs=song)
@app.route('/artists')
def artists():
	artist = session.query(Artist).all()
	return render_template('artists.html', artists=artist)
@app.route('/genres')
def genres():
	return render_template('genres.html')
@app.route('/artist1')
def artist1():
	return render_template('artist1.html')
@app.route('/artist2')
def artist2():
	return render_template('artist2.html')
@app.route('/artist3')
def artist3():
	return render_template('artist3.html')		
@app.route('/year1')
def year1():
	return render_template('year1.html')
@app.route('/year2')
def year2():
	return render_template('year2.html')
@app.route('/year3')
def year3():
	return render_template('year3.html')		
@app.route('/song1')
def song1():
	return render_template('song1.html')
@app.route('/song2')
def song2():
	return render_template('song2.html')
@app.route('/song3')
def song3():
	return render_template('song3.html')	
@app.route('/genre1')
def genre1():
	return render_template('genre1.html')
@app.route('/genre2')
def genre2():
	return render_template('genre2.html')
@app.route('/genre3')
def genre3():
	return render_template('genre3.html')

if __name__ == "__main__":
	app.run()
