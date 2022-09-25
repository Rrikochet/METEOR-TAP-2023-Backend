from flask import render_template, request
from meteorapp import app, db
from meteorapp.models import Household

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