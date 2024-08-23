from flask import Flask, render_template, request, redirect, url_for, flash, current_app
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, UserPreferences
from tmdb_utils import get_trending_movies, get_movie_recommendations, get_movies_by_genre, get_movies_by_rating
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@app.route('/home')
@login_required
def home():
    print("TMDB API Key:", current_app.config['TMDB_API_KEY'])  # For debugging

    # Fetch the user's disliked movies from preferences
    user_pref = UserPreferences.query.filter_by(user_id=current_user.id).first()
    disliked_movies = set()
    if user_pref and user_pref.movie_ratings:
        disliked_movies = set(int(movie_id) for movie_id, rating in user_pref.movie_ratings.items() if rating == 'thumbs_down')

    # Fetch trending movies
    trending_movies = get_trending_movies()

    # Filter out disliked movies
    trending_movies = [movie for movie in trending_movies if movie['id'] not in disliked_movies]

    print(trending_movies)  # Print the result for debugging
    return render_template('home.html', trending_movies=trending_movies)




@app.route('/thumbs_action', methods=['POST'])
@login_required
def thumbs_action():
    movie_id = int(request.form.get('movie_id'))
    action = request.form.get('action')

    user_pref = UserPreferences.query.filter_by(user_id=current_user.id).first()

    if action == 'thumbs_down':
        # Update movie ratings in the JSON column
        if user_pref:
            movie_ratings = user_pref.movie_ratings or {}
            movie_ratings[str(movie_id)] = 'thumbs_down'
            user_pref.movie_ratings = movie_ratings
            db.session.commit()
            flash(f'You disliked movie with ID {movie_id}. It has been recorded.', 'info')

    return redirect(url_for('home'))







@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created for you!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/set_preferences', methods=['GET', 'POST'])
@login_required
def set_preferences():
    if request.method == 'POST':
        genre_id = request.form.get('genre_id')
        min_rating = request.form.get('min_rating')

        if genre_id and min_rating:
            user_pref = UserPreferences.query.filter_by(user_id=current_user.id).first()
            if user_pref:
                user_pref.genre_id = genre_id
                user_pref.min_rating = min_rating
            else:
                user_pref = UserPreferences(user_id=current_user.id, genre_id=genre_id, min_rating=min_rating)
                db.session.add(user_pref)
            db.session.commit()
            flash('Preferences updated successfully!', 'success')
        else:
            flash('Please fill in all fields.', 'warning')

    user_pref = UserPreferences.query.filter_by(user_id=current_user.id).first()
    return render_template('set_preferences.html', user_pref=user_pref)


@app.route('/recommendations/<int:movie_id>')
@login_required
def recommendations(movie_id):
    recommendations = get_movie_recommendations(movie_id)
    return render_template('recommendations.html', recommendations=recommendations)

@app.route('/movies_by_genre', methods=['GET', 'POST'])
@login_required
def movies_by_genre():
    if request.method == 'POST':
        genre_id = request.form.get('genre_id')
        if not genre_id:
            flash('Please select a genre.', 'warning')
            return redirect(url_for('movies_by_genre'))
        movies = get_movies_by_genre(genre_id)
        return render_template('movies_by_genre.html', movies=movies)
    return render_template('genre_input.html')

@app.route('/movies_by_rating', methods=['GET', 'POST'])
@login_required
def movies_by_rating():
    if request.method == 'POST':
        min_rating = request.form.get('min_rating')
        if min_rating:
            try:
                min_rating = float(min_rating)  # Ensure it is a number
            except ValueError:
                flash('Invalid rating value', 'danger')
                return redirect(url_for('movies_by_rating'))
            movies = get_movies_by_rating(min_rating)
            return render_template('movies_by_rating.html', movies=movies, min_rating=min_rating)
        flash('Please provide a rating.', 'warning')
        return redirect(url_for('movies_by_rating'))
    return render_template('rating_input.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/categories')
def categories():
    return render_template('categories.html')


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


@app.route('/test_db')
def test_db():
    try:
        users = User.query.all()
        return f"Database connection successful! Found {len(users)} users."
    except Exception as e:
        return f"Database connection failed: {str(e)}"

@app.route('/logout')
def logout():
    logout_user()
    return render_template('logout.html')

@app.route('/load_user/<int:user_id>')
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)