# For me and error testing
from flask import Flask
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

try:
    db.init_app(app)
    print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed: {e}")
