from flask import Flask, render_template

app = Flask(__name__)

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
