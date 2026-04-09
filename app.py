from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
from models import db, Movie
import os
import requests
#Verstecken API KEY-holen
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager() # Create an object of your DataManager class

@app.route('/', methods = ["GET"])
def home():
    users = data_manager.get_users()
    return render_template('index.html', users=users), 200

@app.route('/users', methods=["POST"])
def create_user():
    user = request.form.get("name")
    data_manager.create_user(user)
    return redirect(url_for('home')), 302

@app.route('/users/<int:user_id>/movies', methods=["GET"])
def get_movies(user_id):
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id)

@app.route('/users/<int:user_id>/movies', methods=["POST"])
def add_movies(user_id):
    movie = request.form.get("movie")

    #Daten von der API holen
    movie_data = get_data_from_api(movie)
    #Aus diesen Daten ein Movieobjekt erstellen
    movie_to_add = create_movie_object(movie_data)

    #Film zur Datenbbank hinzufügen
    data_manager.add_movie(movie_to_add)
    # Film mit dem User verlinken
    user = data_manager.get_single_user(user_id)
    user.movies.append(movie_to_add)

    db.session.commit()

    return redirect(url_for('get_movies', user_id=user_id)), 302

def get_data_from_api(movie_title):
    """Hilfsfunktion für add_movie um die Daten von der Api zu holen"""
    api_key = os.getenv('OMDB_API_KEY')
    address = f"http://www.omdbapi.com/?apikey={api_key}&t={movie_title}"
    #Antwort von API holen
    response = requests.get(address)
    if response.ok:
        #Antwort in json umwandeln
        data = response.json()
        if data['Response'] == 'True':
            return data
        return None



def create_movie_object(data):
    """Hilfsfunktion für add_movie um die Daten in ein MovieObjekt umzuwandeln"""
    new_movie_object = Movie(name=data['Title'], director=data['Director'], year=data['Year'], poster_url=data['Poster'])
    return new_movie_object

@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(movie_id, user_id):
    data_manager.delete_movie(movie_id)

    return redirect(url_for('get_movies', user_id=user_id)), 302

@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    if request.method == "GET":
        movie = data_manager.get_specific_movie(movie_id)
        return render_template('update_movie.html', movie=movie, user_id=user_id, movie_id=movie_id)

    if request.method == "POST":
        new_title = request.form.get("title")
        data_manager.update_movie(movie_id, new_title)

        return redirect(url_for('get_movies', user_id=user_id)), 302




if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)

