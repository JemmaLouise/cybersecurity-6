# Current TMDb APIs being used
import requests
from flask import current_app


def get_tmdb_url(endpoint):
    base_url = 'https://api.themoviedb.org/3'
    return f"{base_url}/{endpoint}"


def get_trending_movies():
    url = get_tmdb_url('trending/movie/day')
    params = {'api_key': current_app.config['TMDB_API_KEY']}
    response = requests.get(url, params=params)
    return response.json()


def get_movie_recommendations(movie_id):
    url = get_tmdb_url(f'movie/{movie_id}/recommendations')
    params = {'api_key': current_app.config['TMDB_API_KEY']}
    response = requests.get(url, params=params)
    return response.json()


def get_movies_by_genre(genre_id):
    url = get_tmdb_url('discover/movie')
    params = {
        'api_key': current_app.config['TMDB_API_KEY'],
        'with_genres': genre_id
    }
    response = requests.get(url, params=params)
    return response.json()


def get_movies_by_rating(min_rating):
    url = get_tmdb_url('discover/movie')
    params = {
        'api_key': current_app.config['TMDB_API_KEY'],
        'vote_average.gte': min_rating
    }
    response = requests.get(url, params=params)
    return response.json()
