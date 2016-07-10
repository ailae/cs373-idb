from flask import Flask, render_template, jsonify, abort
from models import *
from sqlalchemy.orm import sessionmaker
import ast

def artists_and_songs(session):
	json = open('JSON/songs.txt', 'r').read()
	songs = ast.literal_eval(json)
	json2 = open('JSON/artists.txt', 'r').read()
	artists = ast.literal_eval(json2)
	json3 = open('JSON/genre_descriptions.txt', 'r').read()
	genres = ast.literal_eval(json3)
	json4 = open('JSON/years.txt', 'r').read()
	years = ast.literal_eval(json4)
	json5 = open('JSON/artist_genres.txt', 'r').read()
	artist_genres = ast.literal_eval(json5)
	json6 = open('JSON/related_genres.txt', 'r').read()
	related_genres = ast.literal_eval(json6)

	try:
		if not session.query(Artist).first():
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
			if not a.charted_songs:
				for s in session.query(Song).filter_by(artist_id = a.artist_id).all():
					a.charted_songs.append(s)
				# print a.artist_id
				# print s.artist.artist_id
				# s.artist = a
		
		if not session.query(Genre).first():
			for g in genres:
				genre = Genre(name=g['name'], description=g['summary'])
				session.add(genre)
				session.commit()

		if not session.query(Year).first():
			for y in years:
				if not session.query(Artist).filter_by(artist_id=y['top_album_artist_id']).first():
					year = Year(year=y['year'], top_album_name=y['top_album_name'], 
						top_album_id=y['top_album_id'],
						top_genre_name=y['top_genre_name'])
				else:
					year = Year(year=y['year'], top_album_name=y['top_album_name'], 
						top_album_id=y['top_album_id'],
						top_genre_name=y['top_genre_name'], 
						top_album_artist_id=y['top_album_artist_id'])
				session.add(year)
				session.commit()

		# Artist genres relation
		for ag in artist_genres:
			artist = session.query(Artist).filter_by(artist_id=ag['artist_id']).first()
			if not artist.genres:
				for g in ag['genres']:
					artist.genres.append(session.query(Genre).filter_by(name=g).first())

		# Year top genre relation
		for y in session.query(Year).all():
			if not y.top_genre:
				y.top_genre = session.query(Genre).filter_by(name=y.top_genre_name).first()

		# Related genres relation
		for g in related_genres:
			genre = session.query(Genre).filter_by(name=g['name']).first()
			if genre:
				if not genre.related_genres:
					if g['related']:
						for relations in g['related']:
							result = session.query(Genre).filter_by(name=relations).first()
							if result:
								genre.related_genres.append(result)

	except:
		session.rollback()
		raise

app = Flask(__name__)
engine = db_connect()
create_all_tables(engine)
session_maker = sessionmaker(bind=engine)
session = session_maker()
artists_and_songs(session)

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

			
			# Now we will add this year to the its top genre's years_on_top column.
			# This code assumes the top genre for each year was also added to the
			# genres file--therefore it thinks all genres exist in the database at this
			# point, so it can query for them.
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
@app.route('/songs/<id>')
def song(id):
	s = session.query(Song).filter_by(song_id = id).first()
	return render_template('song1.html', song=s)
@app.route('/artists')
def artists():
	artist = session.query(Artist).all()
	return render_template('artists.html', artists=artist)
@app.route('/artists/<id>')
def artist(id):
	a = session.query(Artist).filter_by(artist_id = id).first()
	return render_template('artist1.html', artist=a)
@app.route('/genres')
def genres():
	return render_template('genres.html')
@app.route('/year1')
def year1():
	return render_template('year1.html')
@app.route('/year2')
def year2():
	return render_template('year2.html')
@app.route('/year3')
def year3():
	return render_template('year3.html')		
@app.route('/genre1')
def genre1():
	return render_template('genre1.html')
@app.route('/genre2')
def genre2():
	return render_template('genre2.html')
@app.route('/genre3')
def genre3():
	return render_template('genre3.html')

@app.route('/api/songs', methods=['GET'])
def get_songs() :
	songs = session.query(Song).all()
	song_names = list()
	for song in songs:
		song_names += [song.song_name]
	return jsonify({'result' : song_names, 'success' : True})
	
@app.route('/api/songs/<string:name>', methods=['GET'])
def get_song_by_name(name) :
	song = session.query(Song).filter_by(song_name=name).first()
	
	if not song :
		abort(400)
	
	return jsonify({'result' : song.dictify(), 'success' : True})
	
@app.route('/api/artists', methods=['GET'])
def get_artists() :
	artists = session.query(Artist).all()
	artist_names = list()
	for artist in artists:
		artist_names += [artist.name]
	return jsonify({'result' : artist_names, 'success' : True})
	
@app.route('/api/artists/<string:name>', methods=['GET'])
def get_artist_by_name(name) :
	artist = session.query(Artist).filter_by(name=name).first()
	
	if not artist :
		abort(400)
	
	return jsonify({'result' : artist.dictify(), 'success' : True})
	
@app.route('/api/genres', methods=['GET'])
def get_genres() :
	genres = session.query(Genre).all()
	genre_names = list()
	for genre in genres:
		genre_names += [genre.name]
	return jsonify({'result' : genre_names, 'success' : True})
	
@app.route('/api/genres/<string:name>', methods=['GET'])
def get_genre_by_name(name) :
	genre = session.query(Genre).filter_by(name=name).first()
	
	if not genre :
		abort(400)
	
	return jsonify({'result' : genre.dictify(), 'success' : True})
	
@app.route('/api/years', methods=['GET'])
def get_years() :
	years = session.query(Year).all()
	year_names = list()
	for year in years:
		year_names += [year.year]
	return jsonify({'result' : year_names, 'success' : True})
	
@app.route('/api/years/<int:year>', methods=['GET'])
def get_year_by_name(year) :
	year_obj = session.query(Year).filter_by(year=year).first()
	
	if not year_obj :
		abort(400)
	
	return jsonify({'result' : year_obj.dictify(), 'success' : True})

if __name__ == "__main__":
	app.run()
