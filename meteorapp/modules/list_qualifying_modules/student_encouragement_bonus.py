from flask import render_template
from sqlalchemy import and_
from meteorapp import app, db
from meteorapp.models import Household, Member
from meteorapp.modules.list_qualifying_modules.calculator_modules.current_calculator import current_calculator
from meteorapp.modules.list_qualifying_modules.calculator_modules.age_calculator import age_calculator

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