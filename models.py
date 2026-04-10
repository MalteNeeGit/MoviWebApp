from flask_sqlalchemy import SQLAlchemy

# Datenbankobjekt zum einfachen bedienen
db = SQLAlchemy()

# Zwischentabelle für many-to-many-beziehungen
user_movies = db.Table('user_movies',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('movie_id', db.Integer,db.ForeignKey('movie.id'))
                       )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    movies = db.relationship('Movie', secondary=user_movies, backref='users')

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(200))
    year = db.Column(db.Integer)
    poster_url = db.Column(db.String(500))



