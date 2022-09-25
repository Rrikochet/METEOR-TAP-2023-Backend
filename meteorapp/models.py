from meteorapp import db

# Classes
class Household(db.Model):

    # Table Name
    __tablename__='households'
    
    # Member Values
    id = db.Column(db.Integer, primary_key=True)
    housingType = db.Column(db.String, nullable=False)
    members = db.relationship('Member', backref='households', lazy=True)
    
    # Constructor
    def __init__ (self, housingType, notify=False):
        self.housingType = housingType
    
    # "To String" Method
    def __repr__(self):
        return f"Household('{self.id}', '{self.housingType}', '{self.members}')"

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
