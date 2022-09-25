from flask import render_template
from sqlalchemy import and_
from meteorapp import app, db
from meteorapp.models import Household, Member
from meteorapp.modules.list_qualifying_modules.calculator_modules.current_calculator import current_calculator
from meteorapp.modules.list_qualifying_modules.calculator_modules.age_calculator import age_calculator

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