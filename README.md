# METEOR TAP 2023 Backend

TAP 2023 Div Tech Assessment - Meteor


## Project Website

This project has been deployed on [Heroku](https://gov-grant.herokuapp.com/).


## Overview

The requirements for this assessment is to create an RESTful API that the purpose of Government Grant Distribution. 
The API will have the ability to enable the creation of the households and its members.
Which in turn enables the categorization and identification of household members that are eligible for the Grants.


## Instructions to Run Project Locally

This project is developed on Python 3.9.13 on Windows 10.

1.	Ensure that you have [Python 3](https://www.python.org/downloads/) installed on your machine. 

2.	[Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) the GitHub [Project](https://github.com/Rrikochet/METEOR-TAP-2023-Backend.git) Repository.

3.	To setup the virtual environment. Type into cmd.

	`python -m venv venv`
	
	
4. 	Activate the virtual environment. Type into cmd.

	`. venv/Scrips/activate`
	
	
5.	Install requirements into venv. Type into cmd.

	`pip install -r requirements.txt`


6.	Make sure you cd to the project's repository. Run the program.

	`run.py`
	
	
The Flask Web Server may now be accessed locally. Type `127.0.0.1:5000` on any browser.
The database will start/generate automatically on server startup.


## How to Test the Project

A rudimentary Frontend has been made accessible to aid in the visualisation of the API.

1. 	Create Household 

	- Route: `/household_create`
	- Type: `POST`
	- Form parameters: 
	 	- housingType (as a dropdown list) `	- landed, 
	 						- condominium, 
	 						- hdb`

	- `127.0.0:5000/create` or [Heroku](gov-grant.herokuapp.com/create)

	![image](https://user-images.githubusercontent.com/103415859/192133563-5bec007f-a3c0-4c34-9475-1345cc6f90b0.png)

	
	Assumptions made household_create:
	
	1. 
	

Assumptions made for the assessment in general:
1. 
	Authentication is not required.


Assumptions made for End-Points specified:
1. a. 
	It is assumed that "create" the household is done automatically, 
	an id (primary key) is given to the newly created household to identify it.
1. b.
	The only Housing Types are mentioned. Landed, Condominium, HDB. 

## Thank You!

Admittedly as this was my first take home assignment, I have 
