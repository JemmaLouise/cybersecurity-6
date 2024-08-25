@app.route('/profile')
@login_required
def profile():
    # Fetch the user's current preferences
    user_pref = UserPreferences.query.filter_by(user_id=current_user.id).first()

    # Determine the genre name based on the genre_id
    genre_names = {
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

    # Get the genre name or default to 'Not Set'
    preferred_genre_name = genre_names.get(user_pref.genre_id, 'Not Set') if user_pref else 'Not Set'

    return render_template('profile.html', user_pref=user_pref, preferred_genre_name=preferred_genre_name)
