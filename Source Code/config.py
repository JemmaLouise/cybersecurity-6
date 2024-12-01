import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/movies'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY') or '5609df2250e4c3355f12c198f1353ca6'
    
    # MySQL connection parameters for ML database
    db_username = "**Your Username" # example, use own username
    db_password = "**Your Password"  # example, use own password
    db_host = "**localhost" # example, depends on how your machine is running
    db_port = "**800" # example, depends on how your machine is running
    db_name = "moviesdataconcat"
