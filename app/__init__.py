from flask import Flask, render_template, jsonify, abort
from models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_
import ast
import subprocess
import requests

# def artists_and_songs(session):
# 	json = open('JSON/songs.txt', 'r').read()
# 	songs = ast.literal_eval(json)
# 	json2 = open('JSON/artists.txt', 'r').read()
# 	artists = ast.literal_eval(json2)
# 	json3 = open('JSON/genre_descriptions.txt', 'r').read()
# 	genres = ast.literal_eval(json3)
# 	json4 = open('JSON/years.txt', 'r').read()
# 	years = ast.literal_eval(json4)
# 	json5 = open('JSON/artist_genres.txt', 'r').read()
# 	artist_genres = ast.literal_eval(json5)
# 	json6 = open('JSON/related_genres.txt', 'r').read()
# 	related_genres = ast.literal_eval(json6)
# 	json7 = open('JSON/all_songs_association.txt', 'r').read()
# 	year_song = ast.literal_eval(json7)

# 	try:
# 		if not session.query(Artist).first():
# 			for a in artists:
# 				artist = Artist(name=a['name'], num_followers=a['num_followers'], 
# 				artist_id=a['artist_id'], image_url=a['image_url'], 
# 				popularity=a['popularity'])
# 				session.add(artist)
# 				session.commit()

# 		# Now, make an association between the artist and their genres.
# 		# artist_genres = a['genres']
# 		# for a_genre in artist_genres:
# 		# 	genre_to_add = session.query(Genre).filter_by(name=a_genre).first()
# 		# 	artist.genres.append(genre_to_add)

# 		for s in songs:  
# 			test_song = session.query(Song).filter_by(song_id=s['song_id']).first()
# 			if not test_song:
# 				song = Song(song_id = s['song_id'], song_name = s['song_name'],
# 					artist_id = s['artist_id'], artist_name = s['artist_name'], 
# 					album_name = s['album_name'], explicit = s['explicit'], 
# 					popularity = s['popularity'])
# 				session.add(song)
# 				session.commit()

# 		# Make the charted_songs and artist relationship
# 		for a in session.query(Artist).all():
# 			if not a.charted_songs:
# 				for s in session.query(Song).filter_by(artist_id = a.artist_id).all():
# 					a.charted_songs.append(s)

# 				# s.artist = a
		
# 		if not session.query(Genre).first():
# 			for g in genres:
# 				genre = Genre(name=g['name'], description=g['summary'])
# 				session.add(genre)
# 				session.commit()

# 		if not session.query(Year).first():
# 			for y in years:
# 				if not session.query(Artist).filter_by(artist_id=y['top_album_artist_id']).first():
# 					year = Year(year=y['year'], top_album_name=y['top_album_name'], 
# 						top_album_id=y['top_album_id'],
# 						top_genre_name=y['top_genre_name'])
# 				else:
# 					year = Year(year=y['year'], top_album_name=y['top_album_name'], 
# 						top_album_id=y['top_album_id'],
# 						top_genre_name=y['top_genre_name'], 
# 						top_album_artist_id=y['top_album_artist_id'])
# 				session.add(year)
# 				session.commit()

# 		# Artist genres relation
# 		for ag in artist_genres:
# 			artist = session.query(Artist).filter_by(artist_id=ag['artist_id']).first()
# 			if not artist.genres:
# 				for g in ag['genres']:
# 					artist.genres.append(session.query(Genre).filter_by(name=g).first())
# 					session.commit()

# 		# Year top genre relation
# 		for y in session.query(Year).all():
# 			if not y.top_genre:
# 				y.top_genre = session.query(Genre).filter_by(name=y.top_genre_name).first()
# 				session.commit()

# 		# Related genres relation
# 		for g in related_genres:
# 			genre = session.query(Genre).filter_by(name=g['name']).first()
# 			if genre:
# 				if not genre.related_genres:
# 					if g['related']:
# 						for relations in g['related']:
# 							result = session.query(Genre).filter_by(name=relations).first()
# 							if result:
# 								genre.related_genres.append(result)
# 								session.commit()

# 		# Year song association
# 		for ys in year_song:
# 			# Get the year
# 			year = session.query(Year).filter_by(year = ys['year']).first()
# 			if not year.top_songs:
# 				# Loop through the list of songs
# 				for s in ys['song_list']:
# 					if s['song_id']:
# 						song = session.query(Song).filter_by(song_id = s['song_id']).first()
# 						# Do we have this song in the DB?
# 						if song:
# 							assoc = YearsSongsAssociation(year_num = year.year, 
# 								song_id = s['song_id'], rank= s['rank'])
# 							assoc.song = song
# 							assoc.year = year
# 							year.top_songs.append(assoc)
# 							session.add(assoc)
# 							session.commit()
# 							#song.years_charted.append(assoc) # Do we need this?

# 	except:
# 		session.rollback()
# 		raise

app = Flask(__name__)
# engine = db_connect()
# create_all_tables(engine)
# session_maker = sessionmaker(bind=engine)
# session = session_maker()
# artists_and_songs(session)

@app.route('/')
def homepage():
	return render_template('index.html')
@app.route('/about')
def about():
	return render_template('about.html')
@app.route('/years')
def years():
	year = session.query(Year).all()
	return render_template('years.html', years=year)
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
	genre = session.query(Genre).all()
	return render_template('genres.html', genres=genre)
@app.route('/years/<year>')
def year(year):
	y = session.query(Year).filter_by(year = year).first()
	a = session.query(Artist).filter_by(artist_id = y.top_album_artist_id).first()
	return render_template('year1.html', year=y, artist=a)		
@app.route('/genres/<name>')
def genre(name):
	g = session.query(Genre).filter_by(name = name).first()
	return render_template('genre1.html', genre=g)
@app.route('/visualization')
def visualization():
	response = requests.get('http://sweetify.me/api/artists')
	authors = response.json()['result']
	character_counts = dict()
	for author in authors :
		c = author.upper()[0]
		if c in character_counts :
			character_counts[c] += 1
		else :
			character_counts[c] = 1

	character_counts = [{'text':key,'count':str(character_counts[key])} for key in character_counts]
	
	return render_template('visualization.html', character_counts=character_counts)

@app.route('/search/<term>')
def search(term):
	# Parse it
	term = term.lower()
	terms = term.split()
	# Query
	# queryAndArtist =
	# session.query(Artist).filter(and_(Artist.tsvector_col.match(s) for s in
	# terms))

	queryAndArtist = session.query(Artist, func.ts_headline('english', Artist.name, func.plainto_tsquery(term)).label('h_name')) \
					.filter(and_(Artist.tsvector_col.match(s) for s in terms)).all()

	queryOrArtist = session.query(Artist, func.ts_headline('english', Artist.name, func.plainto_tsquery(term)).label('h_name')) \
					.filter(or_(Artist.tsvector_col.match(s) for s in terms)).all()

	# queryAndSong =
	# session.query(Song).filter(and_(Song.tsvector_col.match(s) for s in
	# terms)).all()
	# queryOrSong = session.query(Song).filter(or_(Song.tsvector_col.match(s)
	# for s in terms)).all()
	queryAndSong = session.query(Song,
								 func.ts_headline('english', Song.song_name,
								                  func.plainto_tsquery(term)).label('h_song_name'),
								 func.ts_headline('english', Song.album_name, func.plainto_tsquery(term)).label('h_album_name')) \
								 .filter(and_(Song.tsvector_col.match(s) for s in terms)).all()


	queryOrSong = session.query(Song, \
								func.ts_headline('english', Song.song_name, func.plainto_tsquery(term)).label('h_song_name'), \
								func.ts_headline('english', Song.album_name, func.plainto_tsquery(term)).label('h_album_name')) \
								.filter(or_(Song.tsvector_col.match(s) for s in terms)).all()

	# queryAndYear = session.query(Year).filter(and_(Year.tsvector_col.match(s) for s in terms)).all()

	# queryOrYear = session.query(Year).filter(or_(Year.tsvector_col.match(s) for s in terms)).all()

	queryAndYear = session.query(Year, \
								 func.ts_headline('english', Year.year, func.plainto_tsquery(term)).label('h_year'), \
								 func.ts_headline('english', Year.top_album_name, func.plainto_tsquery(term)).label('h_top_album_name')) \
								 .filter(and_(Year.tsvector_col.match(s) for s in terms)).all()

	queryOrYear = session.query(Year, \
								 func.ts_headline('english', Year.year, func.plainto_tsquery(term)).label('h_year'), \
								 func.ts_headline('english', Year.top_album_name, func.plainto_tsquery(term)).label('h_top_album_name')) \
								 .filter(or_(Year.tsvector_col.match(s) for s in terms)).all()

	queryAndGenre = session.query(Genre, \
								  func.ts_headline('english', Genre.name, func.plainto_tsquery(term)).label('h_name'), \
								  func.ts_headline('english', Genre.description, func.plainto_tsquery(term)).label('h_description')) \
								  .filter(and_(Genre.tsvector_col.match(s) for s in terms)).all()

	queryOrGenre = session.query(Genre, \
								 func.ts_headline('english', Genre.name, func.plainto_tsquery(term)).label('h_name'), \
								 func.ts_headline('english', Genre.description, func.plainto_tsquery(term)).label('h_description')) \
							     .filter(or_(Genre.tsvector_col.match(s) for s in terms)).all()

	return render_template('search.html', andArtist = queryAndArtist, orArtist = queryOrArtist,
		andSong = queryAndSong, orSong = queryOrSong,
		andYear = queryAndYear, orYear = queryOrYear,
		andGenre = queryAndGenre, orGenre = queryOrGenre)



# API CALLS #
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

@app.route('/api/run_tests', methods=['GET'])
def run_tests():
	try:
		result = subprocess.check_output("python3 tests.py", stderr=subprocess.STDOUT, shell=True)
		return result
	except Exception as e:
		return str(e)

if __name__ == "__main__":
	app.run()