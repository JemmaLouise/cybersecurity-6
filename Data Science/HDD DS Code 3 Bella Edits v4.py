#import general modules 
import pandas as pd
import requests
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
from nltk.sentiment import SentimentIntensityAnalyzer
from sqlalchemy import create_engine, ForeignKey, Column, MetaData, String, Integer, CHAR 
from sqlalchemy import text
from surprise import Dataset, Reader
from surprise import SVD
import os
from pandas import api
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, jsonify, request, requests
from flask_restful import Api, Resource
from flask_cors import CORS # type: ignore
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#Step 1: Create SQLAlchemy Model

# Initialize Flask app and API
app = Flask(__name__)
api = Api(app)
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable CORS for all domains on all routes
CORS(app)

#database creation
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'movies.db')
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initialise database
db = SQLAlchemy(app)

#Initialise Marshallow 
ma = Marshmallow (app)

#create Class for Model
class moviedatabase(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     movie_id = db.Column(db.Integer, unique=True)
     yrmade= db.Column(db.Integer)
     votes= db.Column(db.Integer)
     title = db.Column(db.String(600), unique=True)
     overview = db.Column(db.String(20000))      
     tags = db.Column(db.String(20000))
     genres = db.Column(db.String(20000))
     actors = db.Column(db.String(20000))
     isAdult = db.Column(db.String(200))      
     company = db.Column(db.String(2000))     
     ageRating = db.Column(db.String(200))
     runtime = db.Column(db.Float)
     ratingavgscore = db.Column(db.Float)
         
    #define Model parameters
def __init__(self, id, movie_id, yrmade, votes, title, overview, tags, genres, actors, isAdult, company, ageRating, runtime, ratingavgscore):
    self.id = id
    self.movie_id = movie_id
    self.yrmade = yrmade
    self.votes = votes
    self.title = title
    self.overview = overview
    self.tags = tags
    self.genres = genres
    self.actors = actors
    self.isAdult = isAdult
    self.company = company
    self.ageRating = ageRating
    self.runtime = runtime 
    self.ratingavgscore = ratingavgscore
        
class MovieSchema(ma.Schema):
    class Meta:
        fields = (id, movie_id, yrmade, votes, title, overview, tags, genres, actors, isAdult, company, ageRating, runtime, ratingavgscore) # type: ignore

#initialise Schema 
movie_schema = MovieSchema(strict=True)
movies_schema = MovieSchema(many=True, strict=True)

# Step 2: Load data from CSV files to db

#import modules for SQLAlchemy db with csv files 
import pandas as pd
from numpy import genfromtxt
from time import time
from sqlalchemy import Column, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#create function for loading data from csv files
def Load_Data(file_name):
    data = genfromtxt(file_name, delimiter=',', skip_header=1, converters={0: lambda s: str(s)})
    return data.tolist()

#set base
Base = declarative_base()

#create class for the base
class movieDatabase(Base):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __tablename__ = 'Movie_Database'
    __table_args__ = {'sqlite_autoincrement': True}
    #tell SQLAlchemy the name of column and its attributes:
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, unique=True)
    yrmade= Column(Integer)
    votes= Column(Integer)
    title = Column(str(600), unique=True)
    overview = Column(str(20000)) 
    releaseDate = Column(str(20000))      
    tags = Column(str(20000))
    genres = Column(str(20000))
    actors = Column(str(20000))
    isAdult = Column(str(200))      
    company = Column(str(2000))  
    director = Column(str(2000))     
    ageRating = Column(str(200))
    runtime = Column(Float)
    ratingavgscore = Column(Float)

if __name__ == "__main__":
    t = time()

    #Create the database
    engine = create_engine('sqlite:///movies.db')
    Base.metadata.create_all(engine)

    #Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

     #load csv data into SQLAlchemy model using LoadData function
    try:
        file_name1 = r"datasets\40yrskaggle\movies.csv"
        data = Load_Data(file_name1)
        print (data)
        for a in data:
            record = movieDatabase(**{
                'title':a[0],
                'ageRating' : a[1],
                'genres' : a[2],
                'releaseDate' : a[3],
                'ratingavgscore' : a[4],
                'votes' : a[5],
                'director':a[6],
                'actors' : a[8],
                'company' : a[12],
                'runtime' : a[13],
                
            })
            s.add(record) #Add all the records

        s.commit() #Attempt to commit all the records
        
        file_name2 = r"datasets\imdb\title.basics.tsv\title.basics.tsv" 
        data = Load_Data(file_name2)

        for b in data:
            record = movieDatabase(**{
                'movie_id': b[0],
                'title':b[2],
                'isAdult' : b[4],
                'genres' : b[8],
                'runtime' : b[7],
            })
            s.add(record) #Add all the records

        s.commit() #Attempt to commit all the records
    
   
        file_name3 = r"datasets\imdb\title.ratings.tsv\title.ratings.tsv" 
        data = Load_Data(file_name3)

        for c in data:
            record = movieDatabase(**{
                'ratingavgscore':c[2],
                'votes' : c[3],
                'movie_id' : c[0],
            })
            s.add(record) #Add all the records

        s.commit() #Attempt to commit all the records

        
        file_name4 = r"datasets/movielens/ml-latest-small/ml-latest-small/movies.csv"
        data = Load_Data(file_name4)

        for d in data:
            record = movieDatabase(**{
                'title':d[1],
                'genres' : d[2],
                'movie_id' : d[0],
            })
            s.add(record) #Add all the records

        s.commit() #Attempt to commit all the records
    
        file_name5 = r"datasets\movielens\ml-latest-small\ml-latest-small\ratings.csv"
        data = Load_Data(file_name5)

        for e in data:
            record = movieDatabase(**{
                'ratingavgscore':e[2],
                'movie_id' : e[1],
            })
            s.add(record) #Add all the records

            s.commit() #Attempt to commit all the records

    
    
        file_name6 = r"datasets/movielens/ml-latest-small/ml-latest-small/tags.csv"
        data = Load_Data(file_name6)

        for f in data:
            record = movieDatabase(**{
                'tags':f[2],
                'movie_id' : f[1],
            })
            s.add(record) #Add all the records

        s.commit() #Attempt to commit all the records
    
    
        file_name8 = r"datasets\netflix\netflix_movies_and_tv_shows_sample_dataset_sample.csv" 
        data = Load_Data(file_name8)

        for h in data:
            record = movieDatabase(**{
                'title':h[1],
                'ageRating' : h[4],
                'genres' : h[5],
                'director':h[10],
                'actors' : h[9],
                'overview': h[3],
                'movie_id': h[19],
                
            })
            s.add(record) #Add all the records

        s.commit() #Attempt to commit all the records
            
        file_name9= r"datasets\rottentomatoes\rotten_tomatoes_top_movies_2019-01-15.csv" 
        data = Load_Data(file_name9)

        for i in data:
            record = movieDatabase(**{
                'title':i[1],
                'ratingavgscore' : i[2],
                'votes' : i[3],
                'genres':i[4],
                
            })
            s.add(record) #Add all the records

        s.commit() #Attempt to commit all the records 
        
    except:
        s.rollback() #Rollback the changes on error
    finally:
        s.close() #Close the connection



#Step 3: initialise API set-up

# API keys and access tokens
TMDB_API_KEY = '377a4c89c91b7cf97c533abd029337d8'
OMDB_API_KEY = 'cf051f9e' 
TMDB_API_KEY_ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzNzdhNGM4OWM5MWI3Y2Y5N2M1MzNhYmQwMjkzMzdkOCIsIm5iZiI6MTcyMzYzOTM4NS45MTg4NTcsInN1YiI6IjY2YmNhNTY3YWY2NTMxZWI3NDhjODM0OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ypqovIUfMWgu8RGNe6jmJWtGE7SipXUa2s1r-pD8ing'

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# URL for fetching popular movies
url = f'https://api.themoviedb.org/3/movie/popular?language=en-US&page=1'

# Set up headers
headers = {
    'Authorization': f'Bearer {TMDB_API_KEY_ACCESS_TOKEN}'
}

# Fetch popular movies
response = requests.get(url, headers=headers)
data = response.json()

# MySQL connection parameters
db_username = "Your Username"
db_password = "Your Password"
db_host = "localhost"
db_port = 800
db_name = 'moviesdataconcat'

# Define the SQL query 
query = """
    SELECT 
        movie_id,
        genres,
        tags,
    FROM 
        moviedata 

"""

# Step 4 : begin training the MYSQL database model
# Load data from MySQL database and train the model
def train_model():
    # Create SQLAlchemy engine
    
    engine = create_engine('sqlite:///movies.db')
    meta = MetaData(bind=engine) 
    MetaData.reflect(meta) 
    meta.create_all(engine)

    # Fetch data from MySQL
    df = pd.read_sql_query(query, engine)

    # Convert movie_id to numerical IDs
    label_encoder = LabelEncoder()
    df['movietitle'] = label_encoder.fit_transform(df['title'])
    df.drop(columns=['title'], inplace=True)

    reader = Reader(rating_scale=(1, 5))
    # Load the dataframe into Surprise's Dataset format
    data = Dataset.load_from_df(df, reader)
    
    # Train the SVD (Singular Value Decomposition) algorithm
    model = SVD()
    model.fit(data.build_full_trainset())
    
    return model

def get(self, user_id):
        try:
            # Load trained model
            model = train_model()
            # Get top N recommendations for the user
            top_n = 2
            
            # Create SQLAlchemy engine
            engine = create_engine(f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}")

            # Fetch unique category IDs for the products purchased by the given user
            user_query = f"""
                SELECT DISTINCT
                    movie_id
                FROM 
                    'moviedata' 
            """
            user_df = pd.read_sql_query(user_query, engine)
            genres = user_df['genre'].tolist()
            
            # Create a test set for the given user ID
            test_set = [[user_id, movietitle, 0] for movietitle in data]

            # Predict ratings for the test set
            predictions = model.test(test_set)
            
            # Sort the predictions by estimated rating in descending order
            predictions.sort(key=lambda x: x.est, reverse=True)

            # Extract category names from the sorted predictions
            category_names = [self.get_category_name(prediction.iid) for prediction in predictions[:top_n]]

            return jsonify(category_names)
        except Exception as e:
            return str(e), 500

    # Function to fetch category name based on movie ID
def get_moviename(self, movie_id):
        # Convert movie_id to a regular Python integer
    movie_id = int(movie_id)
        
        # Connect to the database
    engine = create_engine(f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}")
        
        # Establish a connection
    connection = engine.connect()
        
        # Query to fetch movie name based on movie ID
    query = text("SELECT title FROM moviedata WHERE movie_id = movie_id")
        
    try:
            # Bind the movie_id parameter to the query
            query = query.bindparams(movie_id=movie_id)
            
            # Execute the query and fetch the category name
            result = connection.execute(query).fetchone()
            
            # Check if a result is found
            if result:
                movie_name= result[0]  # Extract the genre from the result tuple
                return movie_name
            else:
                return "Unknown "  # Return a default value if genre name is not found
    finally:
            # Close the connection
            connection.close()
        # Endpoint to get recommendations for a given movie_ID:
    
#Step 5: Create initial ML model
def get_recommendation():
    # Create SQLAlchemy engine
    engine = create_engine(f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}")

    # Query to fetch trending categories 
    query = """
        SELECT 
            title,
        FROM 
            moviedata
        GROUP BY 
            genre
        ORDER BY 
            yrmade DESC
        LIMIT 5
    """

    # Fetch data from MySQL
    trending_movies_df = pd.read_sql_query(query, engine)

    # Convert DataFrame to JSON
    trending_movies_json = trending_movies_df.to_json(orient='records')

    return trending_movies_json

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

#Step 6: ML model using API(s)

# Movie details
movies = data['results']
movie_list = []

# Genre mapping
genre_mapping = {
    28: 'Action',
    12: 'Adventure',
    16: 'Animation',
    35: 'Comedy',
    80: 'Crime',
    99: 'Documentary',
    18: 'Drama',
    10751: 'Family',
    14: 'Fantasy',
    36: 'History',
    27: 'Horror',
    10402: 'Music',
    9648: 'Mystery',
    10749: 'Romance',
    878: 'Science Fiction',
    10770: 'TV Movie',
    53: 'Thriller',
    10752: 'War',
    37: 'Western'
}

# Fetch cast data for a movie from TMDb API
def fetch_cast_data(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    cast = response.json().get('cast', [])
    return [member['name'] for member in cast[:5]]  # Top 5 cast members

# Fetch additional data from OMDb API (including Rotten Tomatoes scores)
def fetch_omdb_data(imdb_id):
    url = f"http://www.omdbapi.com/?i=tt3896198&apikey=cf051f9e"
    response = requests.get(url)
    return response.json()

# Prepare and enrich the dataset
for movie in movies:
    movie_id = movie.get('id')
    imdb_id = movie.get('id')

    omdb_data = fetch_omdb_data(imdb_id)
    cast_data = fetch_cast_data(movie_id)

    # Enriching with Rotten Tomatoes data
    if 'Ratings' in omdb_data:
        rotten_tomatoes_score = next((rating['Value'] for rating in omdb_data['Ratings'] if rating['Source'] == 'Rotten Tomatoes'), None)
    else:
        rotten_tomatoes_score = None

    # Sentiment Analysis on movie description
    sentiment = sia.polarity_scores(omdb_data.get('Plot', ''))

    # Detailed genre mapping with cast members
    genres = [genre_mapping.get(genre_id, 'Unknown') for genre_id in movie['genre_ids']]

    movie_info = {
        'movie_id': movie['id'],
        'title': movie['title'],
        'genres': ', '.join(genres),
        'cast': ', '.join(cast_data),
        'popularity': movie['popularity'],
        'vote_average': movie['vote_average'],
        'vote_count': movie['vote_count'],
        'rotten_tomatoes_score': rotten_tomatoes_score,
        'sentiment': sentiment['compound'],
        'description': omdb_data.get('Plot', '')
    }
    movie_list.append(movie_info)

# Convert to DataFrame
movie_df = pd.DataFrame(movie_list)

# Display the first few rows
print("Sample movie data:")
print(movie_df[['title', 'genres', 'cast', 'vote_average', 'popularity']].head())

# Create combined features based on genres, cast, description, and popularity
movie_df['combined_features'] = movie_df.apply(
    lambda row: f"{row['genres']} {row['description']} {row['cast']} {row['sentiment']}", axis=1)

# Convert the combined features into a matrix of TF-IDF features
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movie_df['combined_features'])

# Compute the cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to get recommendations based on title
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movie_df.index[movie_df['title'] == title].tolist()[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Top 5 similar movies
    movie_indices = [i[0] for i in sim_scores]
    return movie_df['title'].iloc[movie_indices]

# Recommend movies similar to a specific movie
print(get_recommendations(movie['title']))

# Advanced Feature Engineering: Calculate average ratings considering Rotten Tomatoes and IMDb scores (if available)
def calculate_combined_rating(row):
    ratings = []
    if row['vote_average']:
        ratings.append(row['vote_average'])
    if row['rotten_tomatoes_score']:
        rt_score = float(row['rotten_tomatoes_score'].replace('%', '')) / 10
        ratings.append(rt_score)
    if ratings:
        return sum(ratings) / len(ratings)
    else:
        return None

movie_df['combined_rating'] = movie_df.apply(calculate_combined_rating, axis=1)

# Example usage of advanced feature engineering for hybrid recommendations
def hybrid_recommendation(title, df, cosine_sim):
    recommendations = get_recommendations(title, df, cosine_sim)
    recommendations_df = df[df['title'].isin(recommendations)]
    return recommendations_df.sort_values('combined_rating', ascending=False)['title'].tolist()

# Example usage
print("Hybrid Recommendations with Cast Integration and Advanced Features:")
print(hybrid_recommendation(f'title', movie_df, cosine_sim))

# Step 7: Training and Evaluating a Machine Learning Model

# Prepare the data
X = movie_df[['vote_average', 'popularity', 'combined_rating']].dropna()
y = movie_df['popularity']  # Predicting popularity based on vote average

# Split into training and testing datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on the test set
predictions = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, predictions)
print(f'\nMean Squared Error: {mse}')

# Real-Time Recommendations (Simulated)
def real_time_recommendations(df):
    return df[df['popularity'] > 50].sample(5)['title'].tolist()

print("Real-Time Recommendations:")
print(real_time_recommendations(movie_df))

# Personalized User Interface (Simulated)
def personalized_recommendations(time_of_day, df, cosine_sim):
    if time_of_day in ["morning", "afternoon"]:
        return get_recommendations(f'title', df, cosine_sim)
    else:
        return real_time_recommendations(df)

# Example usage
print("Personalized Recommendations (Evening):")
print(personalized_recommendations("evening", movie_df, cosine_sim))

@app.route('/handle_post', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        request.form.get('movie_id')
        return (hybrid_recommendation(f'title', movie_df, cosine_sim))


if __name__ == " __main__":
    app.run(debug=True)
    
#todolist: 
#   integrate SQL database 
#   clean/scrub dataset - get rid of duplicates by matching them up and enhancing the data
#   integrate preferences data 
#   use re module? 
#   data engineering?
#   plot graphs or something 

# algo functionality:
#   match up the SQL database with the API database 
#       enrich the data quality by finding movieid in database from the APIs     
#   take in preferences from the front end and use that to refine the dataset 
#       (make smaller) shrink dataset to be searched
#   output personalised recommendation
#   endpoint
