from flask import render_template
from meteorapp import app, db
from meteorapp.models import Household, Member

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