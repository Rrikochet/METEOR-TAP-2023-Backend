from flask import render_template
from meteorapp import app, db
from meteorapp.models import Household

@app.route("/listall", methods=["GET", "POST"])
def household_list_all():
    db.create_all()
    listAllMessage = db.session.query(Household).all()
    return render_template('household_list_all.html', listAllMessage= listAllMessage);
