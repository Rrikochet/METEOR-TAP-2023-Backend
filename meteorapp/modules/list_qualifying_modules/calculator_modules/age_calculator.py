from sqlalchemy import extract

# Age Calculator used by listqualifying pages
def age_calculator(Member):
    age_in_months = (extract('year',Member.dob)*12) + (extract('month',Member.dob)) 
    return age_in_months;