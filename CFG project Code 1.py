import requests
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Personal API key and access token from TMDb (Different for each person)
api_key = '377a4c89c91b7cf97c533abd029337d8'
access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzNzdhNGM4OWM5MWI3Y2Y5N2M1MzNhYmQwMjkzMzdkOCIsIm5iZiI6MTcyMzYzOTM4NS45MTg4NTcsInN1YiI6IjY2YmNhNTY3YWY2NTMxZWI3NDhjODM0OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ypqovIUfMWgu8RGNe6jmJWtGE7SipXUa2s1r-pD8ing'

# URL for fetching popular movies
url = f'https://api.themoviedb.org/3/movie/popular?language=en-US&page=1'

# Set up headers with the access token
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Fetch popular movies
response = requests.get(url, headers=headers)
data = response.json()

# Movie details
movies = data['results']
movie_list = []

for movie in movies:
    movie_info = {
        'movie_id': movie['id'],
        'title': movie['title'],
        'genre_ids': movie['genre_ids'],
        'popularity': movie['popularity'],
        'vote_average': movie['vote_average'],
        'release_date': movie['release_date']
    }
    movie_list.append(movie_info)

# Convert to DataFrame
movie_df = pd.DataFrame(movie_list)

# genre mapping
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

# Create a new column with genre names
movie_df['genres'] = movie_df['genre_ids'].apply(lambda ids: [genre_mapping.get(id, 'Unknown') for id in ids])
movie_df['genres'] = movie_df['genres'].apply(lambda genres: ', '.join(genres))

# Display the first few rows
print("Sample movie data:")
print(movie_df[['title', 'genres', 'vote_average', 'popularity']].head())


# Create features based on genres and popularity
movie_df['features'] = movie_df['genres'] + ' ' + movie_df['popularity'].astype(str)

# Convert the features into a matrix of TF-IDF features
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movie_df['features'])

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

# Step 5: Training and Evaluating a Machine Learning Model

# Prepare the data
X = movie_df[['vote_average', 'popularity']]
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
