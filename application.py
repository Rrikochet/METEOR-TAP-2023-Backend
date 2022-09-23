# Imports
from flask import Flask,redirect, url_for,render_template, url_for, flash, send_from_directory, request, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from datetime import datetime
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

    # Table Name
    __tablename__='households'
    
    # Member Values
    id = db.Column(db.Integer, primary_key=True)
    hType = db.Column(db.String, nullable=False)
    members = db.relationship('Member', backref='households', lazy=True)
    
    # Constructor
    def __init__ (self, hType, notify=False):
        self.hType = hType
    
    # "To String" Method
    def __repr__(self):
        return f"Household('{self.id}', '{self.hType}', '{self.members}')"

# Class Member
class Member(db.Model):
    
    # Table Name
    __tablename__='members'
    
    # Member Values
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    maritalStatus = db.Column(db.String, nullable=False)
    spouse = db.Column(db.Integer, nullable=True)
    occupationType = db.Column(db.String, nullable=False)
    annualIncome = db.Column(db.Float, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    household_id = db.Column(db.Integer, db.ForeignKey('households.id'), nullable=False)
    
    # Constructor
    def __init__ (self, name, gender, maritalStatus, spouse, occupationType, annualIncome, dob, household_id, notify=False):
        self.name = name
        self.gender = gender
        self.maritalStatus = maritalStatus
        self.spouse = spouse
        self.occupationType = occupationType
        self.annualIncome = annualIncome
        self.dob = dob
        self.household_id = household_id
    
    # "To String" Method
    def __repr__(self):
        return f"Member('{self.id}', '{self.name}', '{self.gender}', '{self.maritalStatus}', '{self.spouse}', '{self.occupationType}', '{self.annualIncome}', '{self.dob}', '{self.household_id}')"


# Routes
@app.route("/")
def home():
    return render_template("household_create.html")

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
def household_create():
    # If Method is GET
    if request.method == "GET":
        return render_template('household_create.html');
    # If Method is POST
    elif request.method == "POST":
        db.create_all()
        hT = request.form["hType"]
        db.session.add(Household(hType=hT))
        db.session.commit()
        last = str(db.session.query(Household.id).order_by(Household.id.desc()).limit(1).scalar())
        createMessage = 'New " Household ' + last + ' " is created.'
        return render_template('household_create.html', createMessage=createMessage);
    # If Method is anything else
    else: 
        return redirect(url_for("pagenotfound"))
   
@app.route("/addmember")
def household_add_member():
    db.create_all()
    # If Method is POST
    if request.method == "POST":
        try:
            n = request.form["name"]
            g = request.form["gender"]
            mS = request.form["maritalStatus"]
            s = request.form["spouse"]
            oT = request.form["occupationType"]
            aI = request.form["annualIncome"]
            d = request.form["dob"]
            h = request.form["household_id"]
            addMemberMessage = 'Something went wrong.'
            spouseCheck = False
            
            # UNUSED to see all existing households
            # existingHousehold = [id for id, in db.session.query(Household.id)]
            # Do logic to check for all inputs that cannot be empty
            
            # Spouse Check Function
            def spouse_check(mS, s, spouseCheck, addMemberMessage):
                # Spouse Checks
                # Check if member is single, but inputs a spouse, immediately return message
                if mS == "single" and s != "":
                    addMemberMessage ='You cannot be Single and have a Spouse'
                    return spouseCheck, addMemberMessage
                
                # Check if member is married, must have spouse value
                elif mS == "married" and s == "":
                    addMemberMessage='You cannot be Married and have no Spouse'
                    return spouseCheck, addMemberMessage
                
                # Check if member is married and have spouse values
                elif mS == "married" and s != "":
                
                    # Check if spouse has spouse value of new member id
                    if db.session.query(Member.spouse).filter_by(id=s).limit(1).scalar() is not db.session.query(Member.id).order_by(Member.id.desc()).limit(1).scalar()+1:
                    
                        # Check if spouse already exists on some other member
                        if db.session.query(Member.id).filter_by(spouse=s).limit(1).scalar() is not None:
                            addMemberMessage='Your Spouse is taken by another person'
                            return spouseCheck, addMemberMessage
                    
                        # Check if spouse already has spouse
                        elif db.session.query(Member.spouse).filter_by(id=s).limit(1).scalar() is not None:
                            addMemberMessage='Your Spouse has taken another person'
                            return spouseCheck, addMemberMessage
                            
                        else: 
                            spouseCheck = True
                            return spouseCheck, addMemberMessage
                    else: 
                        spouseCheck = True
                        return spouseCheck, addMemberMessage
                else:
                    spouseCheck = True
                    return spouseCheck, addMemberMessage
                    

            # Print Check if error occured
            spouseCheck, addMemberMessage = spouse_check(mS, s, spouseCheck, addMemberMessage)
            if spouseCheck != True:
                return render_template('household_add_member.html', addMemberMessage=addMemberMessage);

            
            # If Member inputs a household value, use it, otherwise use latest household
            if h == "":
                h = float(db.session.query(Household.id).order_by(Household.id.desc()).limit(1).scalar())
            
            # Add Member
            db.session.add(Member(name=n, gender=g, maritalStatus=mS, spouse=s, occupationType=oT, annualIncome=aI, dob=datetime.strptime(d, '%Y-%m-%d'), household_id=h))
            db.session.commit()
            
            # If Add Member was successful, and If Member has spouse, make spouse have member's spouse id as well
            if db.session.query(Member.id).filter_by(id=s).limit(1).scalar() == s:
                db.session.query(Member.id).filter_by(id=s).update({spouse:db.session.query(Member.id).order_by(Member.id.desc()).limit(1).scalar()})
                
            
            last = str(db.session.query(Member.id).order_by(Member.id.desc()).limit(1).scalar())
            addMemberMessage = 'Member ' + last + ' has been created. '
            return render_template('household_add_member.html', addMemberMessage=addMemberMessage);  
        except Exception as e:
            return render_template('household_add_member.html', addMemberMessage=e);
            
    # If Method is anything else
    else: 
        return render_template('household_add_member.html');

@app.route("/listall")
def household_list_all():
    db.create_all()
    # If Method is POST
    if request.method == "POST": 
        listAllMessage = db.session.query(Household).all()
        return render_template('household_list_all.html', listAllMessage= listAllMessage);
    # If Method is anything else
    else: 
        return render_template('household_list_all.html');
        
@app.route("/search")
def household_search():
    db.create_all()
    # If Method is POST
    if request.method == "POST":
        h = request.form["household_id"]
        searchMessage = db.session.query(Household).get(h)
        return render_template('household_search.html', searchMessage= searchMessage);
    # If Method is anything else
    else: 
        return render_template('household_search.html');

@app.route("/listqualifying")
def household_list_qualifying():
    db.create_all()
    # If Method is POST
    if request.method == "POST":
        h = request.form["household_list_qualifying"]
        listQualifyingMessage = db.session.query(Household).get(h)
        return render_template('household_list_qualifying.html', listQualifyingMessage= listQualifyingMessage);
    # If Method is anything else
    else: 
        return render_template('household_list_qualifying.html');


@app.route("/listqualifying/SEB")
def student_encouragement_bonus():
    db.create_all()
    # If Method is POST
    if request.method == "POST":
        return render_template('student_encouragement_bonus.html');
    # If Method is anything else
    else: 
        return render_template('student_encouragement_bonus.html');



if __name__ == "__main__":
    app.run()
    
    
