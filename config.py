import os


# Add in your own details to line 6 (I called the database 'movies')
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY') or '5691975e0ec0ebc572e6952891fa1124'


HOST = 'localhost'
USER = 'user'
PASSWORD = 'password'
DATABASE = 'database'