import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///movies.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

HOST = "localhost"
USER = "root"
PASSWORD = "p0psicl3"
DATABASE = 'movies'