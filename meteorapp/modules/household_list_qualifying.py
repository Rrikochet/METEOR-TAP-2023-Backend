from flask import render_template, request
from meteorapp import app, db

@app.route("/listqualifying", methods=["GET", "POST"])
def household_list_qualifying():
    db.create_all()
    # If Method is POST
    if request.method == "POST":
        return render_template('household_list_qualifying.html');
    # If Method is anything else
    else: 
        return render_template('household_list_qualifying.html');