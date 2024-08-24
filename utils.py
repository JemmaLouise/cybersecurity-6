# Getting genre name for html formatting
def get_genre_name(genre_id):
    genre_dict = {
        "28": "Action",
        "12": "Adventure",
        "16": "Animation",
        "35": "Comedy",
        "80": "Crime",
        "99": "Documentary",
        "18": "Drama",
        "10751": "Family",
        "14": "Fantasy",
        "36": "History",
        "27": "Horror",
        "10402": "Music",
        "9648": "Mystery",
        "10749": "Romance",
        "10770": "Science Fiction",
        "53": "Thriller",
        "10752": "War",
        "37": "Western"
    }
    return genre_dict.get(genre_id, "Unknown Genre")


# Filter out disliked movies
def filter_disliked_movies(movies, disliked_movie_ids):
    return [movie for movie in movies if movie['id'] not in disliked_movie_ids]