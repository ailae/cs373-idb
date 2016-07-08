from flask import Flask, render_template
from models import *
from sqlalchemy.orm import sessionmaker
import ast


TEST_DATA = {
	'name': 'Drake',
	'num_followers':123,
	'artist_id':'abcd',
	'image_url':'http://www.google.com',
	'popularity':72,
	'spotify_url': 'http://www.spotify.com',
}

app = Flask(__name__)
engine = db_connect()
create_all_tables(engine)
session_maker = sessionmaker(bind=engine)
session = session_maker()
json = open('JSON/songs.txt', 'r').read()
songs = ast.literal_eval(json)

try:
	for s in songs:
		song = Song(song_id = s['song_id'], song_name = s['song_name'],
			artist_name = s['artist_name'], album_name = s['album_name'],
			explicit = s['explicit'], popularity = s['popularity'])
		session.add(song)

	#artist = Artist(**TEST_DATA)
	#artist2 = Artist(name='Drake', num_followers=123, artist_id='abcd', image_url='http://www.google.com', popularity=72, spotify_url='http://www.spotify.com')
	#session.add(artist)
	#session.delete(artist2)
	#session.query(Artist).filter(Artist.name=="Drake").delete()
	session.commit()
except: 
	session.rollback()
	raise
finally:
	session.close()

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
	return render_template('songs.html')
@app.route('/artists')
def artists():
	return render_template('artists.html')
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
