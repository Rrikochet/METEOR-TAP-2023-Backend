from flask import render_template, request
from meteorapp import app, db
from meteorapp.models import Household

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