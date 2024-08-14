# Make sure you have all these downloaded to python to run the programme on your end
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from config import Config
from db_utils import _connect_to_db
from forms import RegistrationForm, LoginForm
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from tmdb_utils import get_trending_movies, get_movie_recommendations, get_movies_by_genre, get_movies_by_rating
from models import db, User, UserPreferences
import requests


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

TMDB_API_KEY = '5691975e0ec0ebc572e6952891fa1124'

# Current home page, requires users to log in to use - not an option to create an account
# When logged in, shows a list of currently trending movies but this can be altered
@app.route('/')
@app.route('/home')
@login_required
def home():
    trending_movies = get_trending_movies()
    return render_template('home.html', trending_movies=trending_movies)


# User registration set up with additions to help with debugging as I was having issues with it originally
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST':
        print("Form submitted")  # Check if the form is being submitted

    if form.validate_on_submit():
        print("Form validated")  # Check if the form passes validation
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created for you!', 'success')
        return redirect(url_for('login'))
    else:
        print("Form did not validate")  # Notify that validation failed
        print(form.errors)  # Print the form errors to the console

    return render_template('register.html', form=form)


# Endpoint for users to login, required to see any of the other pages
# Don't think we want there to be a guest option but let me know if so
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
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)


# Users use drop down list to pick 1 genre and min film rating (1-10) to save in a SQL table
# Would be better if they can select multiple genres
@app.route('/set_preferences', methods=['GET', 'POST'])
@login_required
def set_preference():
    if request.method == 'POST':
        genre_id = request.form.get('genre_id')
        min_rating = request.form.get('min_rating')
        if not genre_id or not min_rating:
            flash('Please fill in all fields.', 'warning')
            return redirect(url_for('set_preferences'))

        # Save the user preferences
        user_pref = UserPreferences(user_id=current_user.id, genre_id=genre_id, min_rating=min_rating)
        db.session.add(user_pref)
        db.session.commit()
        flash('Your preferences have been saved!', 'success')
        return redirect(url_for('home'))

    # Render the preference form if GET request
    return render_template('set_preferences.html')

# Needs work with machine learning/ data scientist to give accurate recommendations but the endpoint is created
@app.route('/recommendations/<int:movie_id>')
@login_required
def recommendations(movie_id):
    recommendations = get_movie_recommendations(movie_id)
    return render_template('recommendations.html', recommendations=recommendations)

# Shows top trending movies in that genre
@app.route('/movies_by_genre', methods=['GET', 'POST'])
@login_required
def movies_by_genre():
    if request.method == 'POST':
        genre_id = request.form.get('genre_id')
        if not genre_id:
            flash('Please select a genre.', 'warning')
            return redirect(url_for('movies_by_genre'))

        try:
            url = f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre_id}'
            response = requests.get(url)
            response.raise_for_status()  # Raises HTTPError for bad responses
            movies = response.json()
        except requests.exceptions.RequestException as e:
            flash(f'Error fetching movies: {e}', 'danger')
            return redirect(url_for('movies_by_genre'))

        return render_template('movies_by_genre.html', movies=movies)

    return render_template('genre_input.html')

# Shows top trending movies with a minimum rating between 1-10
@app.route('/movies_by_rating', methods=['GET', 'POST'])
@login_required
def movies_by_rating():
    if request.method == 'POST':
        min_rating = request.form.get('min_rating')
        url = f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&vote_average.gte={min_rating}'
        response = requests.get(url)
        movies = response.json()
        return render_template('movies_by_rating.html', movies=movies, min_rating=min_rating)
    return render_template('rating_input.html')


# Endpoint just for me to test the database is connected
@app.route('/test_db')
def test_db():
    try:
        users = User.query.all()
        return f"Database connection successful! Found {len(users)} users."
    except Exception as e:
        return f"Database connection failed: {str(e)}"


# endpoint to allow users to log out
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Endpoint to see all users so don't have to go to MySQL
@app.route('/users')
@login_required
def users():
    connection = _connect_to_db()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM users"
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(result)


# Ensures users are logged in
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True)
