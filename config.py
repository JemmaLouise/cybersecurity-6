import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///movies.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# make sure to add in your own details for MySQL
HOST = "localhost"
USER = "USER"
PASSWORD = "PASSWORD"
DATABASE = "movies"