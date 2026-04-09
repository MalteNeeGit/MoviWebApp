from models import db, User, Movie

class DataManager():
    # Define Crud operations as methods
    def create_user(self,name):
        """Creates a new user"""
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        """ Returns a list of all users"""
        users = db.session.query(User).all()

        return users

    def get_movies(self, user_id):
        """Gets the movies from a particular user and returns the Movies as a list"""
        user = db.session.query(User)\
        .filter(User.id == user_id).one()

        return user.movies

    def add_movie(self,movie):
        """Adds a movie to the users database"""
        db.session.add(movie)
        db.session.commit()

    def update_movie(self, movie_id, new_title):
        """Updates the title of a Movie"""
        movie_to_update = db.session.query(Movie)\
        .filter(Movie.id == movie_id).one()

        movie_to_update.name = new_title
        db.session.commit()

    def delete_movie(self, movie_id):
        """Deletes a movie from a database"""
        db.session.query(Movie)\
        .filter(Movie.id == movie_id).delete()
        db.session.commit()

    def get_single_user(self,user_id):
        """Catches a single user from the db by id"""
        single_user = db.session.query(User)\
        .filter(User.id == user_id).one()

        return single_user
