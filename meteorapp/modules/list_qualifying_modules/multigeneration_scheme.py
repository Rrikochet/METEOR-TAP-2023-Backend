from flask import render_template
from sqlalchemy import or_ , and_
from meteorapp import app, db
from meteorapp.models import Household, Member
from meteorapp.modules.list_qualifying_modules.calculator_modules.current_calculator import current_calculator
from meteorapp.modules.list_qualifying_modules.calculator_modules.age_calculator import age_calculator

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