import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:p0psicl3@localhost/movies'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY') or '5609df2250e4c3355f12c198f1353ca6'
