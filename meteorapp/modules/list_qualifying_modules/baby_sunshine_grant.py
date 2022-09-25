from flask import render_template
from meteorapp import app, db
from meteorapp.models import Member
from meteorapp.modules.list_qualifying_modules.calculator_modules.current_calculator import current_calculator
from meteorapp.modules.list_qualifying_modules.calculator_modules.age_calculator import age_calculator

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
