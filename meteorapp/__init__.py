# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import secrets
import string

# Important
app = Flask(__name__)
app.secret_key = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(32))
app.permanent_session_lifetime = timedelta(hours=1)

# Create Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

from meteorapp import routes