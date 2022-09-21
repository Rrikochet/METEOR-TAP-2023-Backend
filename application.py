# Imports
from flask import Flask,redirect, url_for,render_template, url_for, flash, send_from_directory, request, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import secrets
import string

# Important
app = Flask(__name__)
key = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(32))
app.secret_key = key
app.permanent_session_lifetime = timedelta(hours=1)

# Create Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
db.create_all()

# Classes
class Household(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hType = db.Column(db.String(20), unique=False, nullable=False)
    
    def __repr__(self):
        return f"Household('{self.id}', '{self.hType}')"
        
# class Member(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(20), unique=False, nullable=False)
    # gender = db.Column(db.String(20), unique=False, nullable=False)
    # maritalStatus = db.Column(db.String(20), unique=False, nullable=False)
    # spouse = db.Column(db.String(20), unique=False, nullable=False)
    # occupationType = db.Column(db.String(20), unique=False, nullable=False)
    # annualIncome = db.Column(db.String(20), unique=False, nullable=False)
    # dob = db.Column(db.String(20), unique=False, nullable=False)
    
    # def __repr__(self):
        # return f"Household('{self.id}', '{self.hType}')"


# Routes
@app.route("/")
def home():
    #return "<h1>Hello</h1>"
    return render_template("index.html")

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.route("/pagenotfound")
def pagenotfound():
    return f"404 Error! Page Not Found"

@app.route("/admin")
def admin():
    return redirect(url_for("pagenotfound"))
    
@app.route("/create")
def display_household_create():
    return render_template('household_create.html');
    
@app.route("/create",methods=["POST"])
def submit_household_create():
    db.create_all()
    hT = request.form["hType"]
    db.session.add(Household(hType=hT))
    db.session.commit()
    last = str(db.session.query(Household).order_by(Household.id.desc()).first())
    createMessage = last + ' has been created. '
    return render_template('household_create.html', createMessage=createMessage);
    
@app.route("/addmember")
def display_household_add_member():
    return render_template('household_add_member.html');    
    
@app.route("/addmember",methods=["POST"])
def submit_household_add_member():
    return render_template('household_add_member.html');   


if __name__ == "__main__":
    app.run()
    
    
