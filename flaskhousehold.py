from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class Household(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hType = db.Column(db.String(20), unique=False, nullable=False)
    
    def __repr__(self):
        return f"Household('{self.id}', '{self.hType}')"
