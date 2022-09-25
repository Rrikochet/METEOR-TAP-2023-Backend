from datetime import datetime
from sqlalchemy import extract

# Current Calculator used by listqualifying pages
def current_calculator(Y, M):
    current_in_months = ((extract('year',datetime.today())-Y)*12) + (extract('month',datetime.today())-M)
    return current_in_months;