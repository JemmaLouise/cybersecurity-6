# Current TMDb APIs being used
import requests
from flask import current_app


def get_tmdb_url(endpoint):
    base_url = 'https://api.themoviedb.org/3/trending/movie/day?api_key=5609df2250e4c3355f12c198f1353ca6'
    return f"{base_url}/{endpoint}"

def get_trending_movies():
    url = 'https://api.themoviedb.org/3/trending/movie/day'
    api_key = current_app.config['TMDB_API_KEY']
    print(f"Using API Key: {api_key}")  # Debugging line
    params = {'api_key': api_key}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print(data)  # For debugging
        return data.get('results', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trending movies: {e}")
        return []

def get_movie_recommendations(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/recommendations'
    api_key = current_app.config['TMDB_API_KEY']
    print(f"Using API Key: {api_key}")  # Debugging line
    params = {'api_key': api_key}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print(data)  # For debugging
        return data.get('results', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movie recommendations: {e}")
        return []


def get_movies_by_genre(genre_id):
    url = 'https://api.themoviedb.org/3/discover/movie'
    api_key = current_app.config['TMDB_API_KEY']
    print(f"Using API Key: {api_key}")  # Debugging line
    params = {
        'api_key': api_key,
        'with_genres': genre_id
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print(data)  # For debugging the entire response
        results = data.get('results', [])
        if not results:
            print(f"No movies found for genre_id: {genre_id}")
        return results
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movies by genre: {e}")
        return []




def get_movies_by_rating(min_rating):
    url = 'https://api.themoviedb.org/3/discover/movie'
    api_key = current_app.config['TMDB_API_KEY']
    print(f"Using API Key: {api_key}")  # Debugging line
    params = {
        'api_key': api_key,
        'vote_average.gte': min_rating
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print(data)  # For debugging the entire response
        results = data.get('results', [])
        if not results:
            print(f"No movies found with rating >= {min_rating}")
        return results
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movies by rating: {e}")
        return []


def get_trending_movies():
    url = 'https://api.themoviedb.org/3/trending/movie/day'
    api_key = current_app.config['TMDB_API_KEY']
    params = {'api_key': api_key}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        trending_movies = response.json().get('results', [])

        # Fetch additional details for each movie
        detailed_movies = []
        for movie in trending_movies:
            movie_id = movie['id']
            details_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=releases'
            details_response = requests.get(details_url)
            details_response.raise_for_status()
            movie_details = details_response.json()
            # Extract age rating
            age_rating = next(
                (country['certification'] for country in movie_details.get('releases', {}).get('countries', []) if
                 country['iso_3166_1'] == 'US'),
                'N/A'
            )
            movie['age_rating'] = age_rating
            detailed_movies.append(movie)

        return detailed_movies

    except requests.exceptions.RequestException as e:
        print(f"Error fetching trending movies: {e}")
        return []

