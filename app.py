from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from config import Config
from db_utils import _connect_to_db
from models import db, User
from forms import RegistrationForm, LoginForm
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    if request.method == 'POST':
        question = request.form.get('question')
        # Process question and make an API call to TMDb as needed
        flash("Your question: {}".format(question), 'info')
    return render_template('ask.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("Form validated successfully!")  # Debug print
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created for you!', 'success')
        return redirect(url_for('login'))
    print("Form not valid:", form.errors)  # Debug print for form errors
    return render_template('register.html', form=form)


@app.route('/test_db')
def test_db():
    try:
        # Try to connect and query the database
        users = User.query.all()
        return f"Database connection successful! Found {len(users)} users."
    except Exception as e:
        return f"Database connection failed: {str(e)}"


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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/users')
@login_required
def users():
    connection = _connect_to_db()  # Use your custom database connection function
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM users"
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(result)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True)
