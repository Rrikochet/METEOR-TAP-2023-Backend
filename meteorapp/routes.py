from flask import redirect, url_for, render_template, url_for, flash, send_from_directory, request, session
from meteorapp.models import Household, Member
from sqlalchemy import exc, extract, func, or_, and_
from datetime import datetime
from meteorapp import app, db
from meteorapp.modules.list_qualifying_modules.calculator_modules.current_calculator import current_calculator
from meteorapp.modules.list_qualifying_modules.calculator_modules.age_calculator import age_calculator

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
    
@app.route("/create", methods=["GET", "POST"])
def household_create():
    # If Method is POST
    if request.method == "POST":
        db.create_all()
        hT = request.form["housingType"]
        db.session.add(Household(housingType=hT))
        db.session.commit()
        last = str(db.session.query(Household.id).order_by(Household.id.desc()).limit(1).scalar())
        createMessage = 'New " Household ' + last + ' " is created.'
        return render_template('household_create.html', createMessage=createMessage);
    # If Method is anything else
    else: 
        return render_template('household_create.html');
   
@app.route("/addmember", methods=["GET", "POST"])
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

            # If Member inputs no annualIncome, it will be 0
            if aI == "":
                aI = 0
            
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

@app.route("/listall", methods=["GET", "POST"])
def household_list_all():
    db.create_all()
    listAllMessage = db.session.query(Household).all()
    return render_template('household_list_all.html', listAllMessage= listAllMessage);

        
@app.route("/search", methods=["GET", "POST"])
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

@app.route("/listqualifying", methods=["GET", "POST"])
def household_list_qualifying():
    db.create_all()
    # If Method is POST
    if request.method == "POST":
        return render_template('household_list_qualifying.html');
    # If Method is anything else
    else: 
        return render_template('household_list_qualifying.html');


@app.route("/listqualifying/SEB", methods=["GET", "POST"])
def student_encouragement_bonus():
    db.create_all()
    filtered_members = []
    household_income = 0
    
    # Join Household and Member
    household_table = db.session.query(Household).join(Member, Household.id == Member.household_id)
    # For each Household
    for row in household_table:
        # For each Member
        for subrow in row.members:
            # Add their incomes together
            household_income = household_income + subrow.annualIncome
        # If income in a household < 200000, create a list of members.id
        if household_income < 200000.0:
            # Track each member in a list
            for subrow in row.members:
                filtered_members.append(subrow.id)
        # Reset to 0 for next household
        household_income = 0
        
    # Filters for Member's id and household_id
        # If age < 16
        # If Household income < 200,000
        # If Member is a student
        # That Member is eligible
        # TO DO - Currently Accurate to Month. Would like higher accuracy
    qualified_members = db.session.query(Member.household_id, Member.id).filter(and_(age_calculator(Member) > current_calculator(16, 0), Member.id.in_(filtered_members), Member.occupationType == 'student')).order_by(Member.household_id.asc()).all()

    SEBMessage = qualified_members
    print("\nBelow are SEB Qualified Members\n")
    for row in SEBMessage:
        print ('Household, Member: ' + str(row), end='\n')
    print("\n")
    return render_template('student_encouragement_bonus.html', SEBMessage=SEBMessage);
     
@app.route("/listqualifying/MS", methods=["GET", "POST"])
def multigeneration_scheme():
    db.create_all()
    qualified_members = []
    filtered_households = []
    household_income = 0

    # Join Household and Member
    household_table = db.session.query(Household).join(Member, Household.id == Member.household_id)
    # For each Household
    for row in household_table:
        # For each Member
        for subrow in row.members:
            # Add their incomes together
            household_income = household_income + subrow.annualIncome
        # If income in a household < 150000, create a list of household.id
        if household_income < 150000.0:
            # Track each householf in a list
            filtered_households.append(row.id)
        # Reset to 0 for next household
        household_income = 0
        
    # Filters for Member's id and household_id
        # If age < 18 or age > 55
        # If Household income < 150,000
        # All Members in Household are eligible
        # TO DO - Currently Accurate to Month. Would like higher accuracy
    filtered_members = db.session.query(Member).filter(and_(or_(age_calculator(Member) > current_calculator(18, 0), age_calculator(Member) < current_calculator(55, 0)), Member.household_id.in_(filtered_households))).order_by(Member.household_id.asc()).all()
    
    # Checks for duplicates in filtered households
    for dupes in filtered_members:
        if dupes not in qualified_members:
            qualified_members.append(dupes.household_id)

    # All members from qualified households
    qualified_households = db.session.query(Member.household_id, Member.id).filter(Member.household_id.in_(qualified_members)).order_by(Member.household_id.asc()).all()

    MSMessage = qualified_households
    print("\nBelow are MS Qualified Members\n")
    for row in MSMessage:
        print ('Household, Member: ' + str(row), end='\n')
    print("\n")
    return render_template('multigeneration_scheme.html', MSMessage=MSMessage);
    
@app.route("/listqualifying/EB", methods=["GET", "POST"])
def elder_bonus():
    db.create_all()
    filtered_households = []

    # Join Household and Member
    household_table = db.session.query(Household).join(Member, Household.id == Member.household_id)
    # For each Household
    for row in household_table:
        # If member is in a hdb household, create a list of members
        if row.housingType == 'hdb':
            # Track each householf in a list
            filtered_households.append(row.id)
        
    # Filters for Member's id and household_id
        # If age > 55
        # If Household is hdb
        # That Member is eligible
        # TO DO - Currently Accurate to Month. Would like higher accuracy
    qualified_members = db.session.query(Member).filter(and_(age_calculator(Member) < current_calculator(55, 0)), Member.household_id.in_(filtered_households)).order_by(Member.household_id.asc()).all()

    EBMessage = qualified_members
    print("\nBelow are EB Qualified Members\n")
    for row in EBMessage:
        print ('Household, Member: ' + str(row), end='\n')
    print("\n")
    return render_template('elder_bonus.html', EBMessage=EBMessage);
    
@app.route("/listqualifying/BSG", methods=["GET", "POST"])
def baby_sunshine_grant():
    db.create_all()
 
    # Filters for Member's id and household_id
        # If age < 8 months
        # That Member is eligible
        # TO DO - Currently Accurate to Month. Would like higher accuracy
    qualified_members = db.session.query(Member).filter(age_calculator(Member) > current_calculator(0, 8)).order_by(Member.household_id.asc()).all()

    BSGMessage = qualified_members
    print("\nBelow are BSG Qualified Members\n")
    for row in BSGMessage:
        print ('Household, Member: ' + str(row), end='\n')
    print("\n")
    return render_template('baby_sunshine_grant.html', BSGMessage=BSGMessage);

@app.route("/listqualifying/YGG", methods=["GET", "POST"])
def yolo_gst_grant():
    db.create_all()
    income_filtered_households = []
    income_qualified_households = []
    housing_filtered_households = []
    housing_qualified_households = []
    qualified_households = []
    household_income = 0

    # Join Household and Member
    household_table = db.session.query(Household).join(Member, Household.id == Member.household_id)
    # For each Household
    for row in household_table:
    
        # For each Member
        for subrow in row.members:
            # Add their incomes together
            household_income = household_income + subrow.annualIncome
        # If income in a household < 100000, create a list of household.id
        if household_income < 100000.0:
            # Track each householf in a list
            income_filtered_households.append(row.id)
        # Reset to 0 for next household
        household_income = 0
        # If household is a hdb, create a list of household.id
        if row.housingType == 'hdb':
            # Track each householf in a list
            housing_filtered_households.append(row.id)
    
    # Checks for duplicates in income filtered households
    for dupes in income_filtered_households:
        if dupes not in income_qualified_households:
            income_qualified_households.append(dupes)
    
    # Then checks for duplicates in housing filtered households
    for dupes in housing_filtered_households:
        if dupes not in housing_qualified_households:
            housing_qualified_households.append(dupes)

    # Then checks for similar in both qualified households
    for similar in income_qualified_households:
        if similar in housing_qualified_households:
            qualified_households.append(similar)

    # Filters for Member's id and household_id
        # If Household income < 100,000
        # If Household is hdb
        # All Members in Household are eligible
        # TO DO - Currently Accurate to Month. Would like higher accuracy
    qualified_members = db.session.query(Member).filter(Member.household_id.in_(qualified_households)).order_by(Member.household_id.asc()).all()

    YGGMessage = qualified_members
    print("\nBelow are YGG Qualified Members\n")
    for row in YGGMessage:
        print ('Household, Member: ' + str(row), end='\n')
    print("\n")
    return render_template('yolo_gst_grant.html', YGGMessage=YGGMessage);
