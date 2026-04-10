import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
from models import db, Movie

# .env Datei laden um API Key zu verstecken
load_dotenv()

# Flask App initialisieren
app = Flask(__name__)

# Datenbankpfad erstellen
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Datenbank mit der App verbinden
db.init_app(app)

# DataManager Objekt erstellen für alle Datenbankoperationen
data_manager = DataManager()


@app.route('/', methods=["GET"])
def home():
    """Startseite zeigt alle Nutzer an."""
    users = data_manager.get_users()
    return render_template('index.html', users=users), 200


@app.route('/users', methods=["POST"])
def create_user():
    """Neuen Nutzer aus dem Formular erstellen."""
    user = request.form.get("name")
    data_manager.create_user(user)
    return redirect(url_for('home')), 302


@app.route('/users/<int:user_id>/movies', methods=["GET"])
def get_movies(user_id):
    """Filmliste eines bestimmten Nutzers anzeigen."""
    movies = data_manager.get_movies(user_id)
    # Errorhandling
    if movies is None:
        return render_template('404.html', user_id=user_id), 404
    return render_template('movies.html', movies=movies, user_id=user_id)


@app.route('/users/<int:user_id>/movies', methods=["POST"])
def add_movies(user_id):
    """Film zur Favoritenliste eines Nutzers hinzufügen."""
    # Zuerst prüfen ob der User existiert
    user = data_manager.get_single_user(user_id)
    if user is None:
        return render_template('404.html', user_id=user_id), 404

    # Filmtitel aus Formular holen
    movie = request.form.get("movie")

    # Daten von der API holen, abbrechen wenn Film nicht gefunden
    movie_data = get_data_from_api(movie)
    if movie_data is None:
        return render_template('404.html', user_id=user_id), 404

    # Film nicht doppelt hinzufügen
    if data_manager.movie_exists(user_id, movie_data['Title']):
        return redirect(url_for('get_movies', user_id=user_id)), 302

    # Film-Objekt erstellen und in Datenbank speichern
    movie_to_add = create_movie_object(movie_data)
    data_manager.add_movie(movie_to_add)

    # Film mit dem User verknüpfen und speichern
    user.movies.append(movie_to_add)
    db.session.commit()

    return redirect(url_for('get_movies', user_id=user_id)), 302


def get_data_from_api(movie_title):
    """HelperFunktion für add_movies: Filmdaten von der OMDb API holen.

    Gibt None zurück wenn der Film nicht gefunden wird
    oder ein HTTP-Fehler auftritt.
    """
    # Versteckten Key holen
    api_key = os.getenv('OMDB_API_KEY')
    address = f"http://www.omdbapi.com/?apikey={api_key}&t={movie_title}"
    # Timeout dafür dass die App ewig wartet wenn API nicht antwortet
    response = requests.get(address, timeout=5)
    if response.ok:
        data = response.json()
        if data['Response'] == 'True':
            return data
        # Film wurde nicht gefunden
        return None
    # HTTP Fehler
    return None


def create_movie_object(data):
    """Aus den API-Daten ein SQLAlchemy Movie-Objekt erstellen."""
    return Movie(
        name=data['Title'],
        director=data['Director'],
        year=data['Year'],
        poster_url=data['Poster']
    )


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(movie_id, user_id):
    """Film aus der Favoritenliste eines Nutzers löschen."""
    data_manager.delete_movie(movie_id)
    return redirect(url_for('get_movies', user_id=user_id)), 302


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """Film-Titel aktualisieren."""
    if request.method == "GET":
        # Film aus DB holen und Update-Formular anzeigen
        movie = data_manager.get_specific_movie(movie_id)
        if movie is None:
            return render_template('404.html', user_id=user_id), 404
        return render_template('update_movie.html', movie=movie, user_id=user_id, movie_id=movie_id)

    # POST – neuen Titel speichern
    new_title = request.form.get("title")
    data_manager.update_movie(movie_id, new_title)
    return redirect(url_for('get_movies', user_id=user_id)), 302


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Nutzer und seine Daten löschen."""
    data_manager.delete_user(user_id)
    return redirect(url_for('home')), 302


@app.errorhandler(404)
def page_not_found(_e):
    """404 Fehler – Seite oder Ressource nicht gefunden."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(_e):
    """500 Fehler – unerwarteter Serverfehler."""
    return render_template('500.html'), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)