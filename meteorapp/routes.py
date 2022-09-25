from flask import redirect, url_for, render_template, flash, send_from_directory, request, session
from sqlalchemy import exc, extract, func, or_, and_
from datetime import datetime
from meteorapp import app, db
from meteorapp.models import Household, Member
from meteorapp.modules.list_qualifying_modules.calculator_modules.current_calculator import current_calculator
from meteorapp.modules.list_qualifying_modules.calculator_modules.age_calculator import age_calculator
from meteorapp.modules.list_qualifying_modules.yolo_gst_grant import yolo_gst_grant
from meteorapp.modules.list_qualifying_modules.baby_sunshine_grant import baby_sunshine_grant
from meteorapp.modules.list_qualifying_modules.elder_bonus import elder_bonus
from meteorapp.modules.list_qualifying_modules.multigeneration_scheme import multigeneration_scheme
from meteorapp.modules.list_qualifying_modules.student_encouragement_bonus import student_encouragement_bonus
from meteorapp.modules.household_list_qualifying import household_list_qualifying
from meteorapp.modules.household_search import household_search
from meteorapp.modules.household_list_all import household_list_all
from meteorapp.modules.household_add_member import household_add_member
from meteorapp.modules.household_create import household_create

# Routes
@app.route("/")
def home():
    return render_template("household_create.html")

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.route("/pagenotfound")
def pagenotfound():
    return f"404 Error! Page Not Found"

@app.route("/admin")
def admin():
    return redirect(url_for("pagenotfound"))