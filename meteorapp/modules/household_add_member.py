from flask import render_template, request
from meteorapp import app, db
from meteorapp.models import Household, Member
from datetime import datetime

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

            # Name cannot be empty
            if n == "":
                return render_template('household_add_member.html', addMemberMessage="Name cannot be Empty");
            
            # Gender must be male or female
            if g != "male" and g != "female":
                return render_template('household_add_member.html', addMemberMessage="You have to be male of female");
            
            # Marital Status and Spouse
            # Check if error occured
            spouseCheck, addMemberMessage = spouse_check(mS, s, spouseCheck, addMemberMessage)
            if spouseCheck != True:
                return render_template('household_add_member.html', addMemberMessage=addMemberMessage);

            # Occupation Type must be employed, unemployed or student
            if oT != "unemployed" and oT != "employed" and oT != "student":
                return render_template('household_add_member.html', addMemberMessage="You have to be employed, unemployed, or student");

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


 # Spouse Check Function
def spouse_check(mS, s, spouseCheck, addMemberMessage):
    # Spouse Checks
    
    # Check if member marries him/herself
    if mS == 'married' and s == Member.id:
        addMemberMessage ='You cannot marry yourself'
        return spouseCheck, addMemberMessage
    
    # Check if member is single, but inputs a spouse, immediately return message
    elif mS == "single" and s != "":
        addMemberMessage ='You cannot be Single and have a Spouse'
        return spouseCheck, addMemberMessage
    
    # Check if member is married, must have spouse value
    elif mS == "married" and s == "":
        addMemberMessage='You cannot be Married and have no Spouse'
        return spouseCheck, addMemberMessage
     
    # Check if member is married and have spouse values and have same household id
    elif mS == "married" and s != "" and db.session.query(Member.household_id).filter_by(id=s) != db.session.query(Member.household_id).filter_by(id=id):
        # Check if spouse has spouse value of new member id
        if db.session.query(Member.id).order_by(Member.id.desc()).limit(1).scalar() is None:
            x = 1
        else :
            x = db.session.query(Member.id).order_by(Member.id.desc()).limit(1).scalar() + 1
            
            
        if db.session.query(Member.spouse).filter_by(id=s).limit(1).scalar() is not x:
        
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
            addMemberMessage='Your Spouse is not your spouse'
            return spouseCheck, addMemberMessage
        
    elif mS == "married" and s != "" and db.session.query(Member.household_id).filter_by(id=s) == db.session.query(Member.household_id).filter_by(id=id):
        spouseCheck = True
        return spouseCheck, addMemberMessage
    else:
        spouseCheck = True
        return spouseCheck, addMemberMessage
    
       
