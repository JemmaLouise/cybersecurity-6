import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from nltk.sentiment import SentimentIntensityAnalyzer

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
print("\nRecommendations for 'Inception':")
print(get_recommendations('Inception'))

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
print(hybrid_recommendation("Inception", movie_df, cosine_sim))

# Step 5: Training and Evaluating a Machine Learning Model

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
        return get_recommendations("Inception", df, cosine_sim)
    else:
        return real_time_recommendations(df)

# Example usage
print("Personalized Recommendations (Evening):")
print(personalized_recommendations("evening", movie_df, cosine_sim))
