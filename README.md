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
On the top of every page is a button to redirect you to their respective page.
1 	to  	5 	Are the 5 API End-Points as set by the requirements. The endpoints use URL path and HTTP verbs.
5. 1 	to 	5. 5	Are the 5 Grants as part of the Government Grant Disbursement API per no. 5.


1. 	Create Household 

	- Route: `/household_create`
	- Type: `POST`
	- Form parameters: 
	 	- housingType (as a dropdown list) `landed, condominium, hdb`
	- `127.0.0:5000/create` or [Heroku](https://gov-grant.herokuapp.com/create)

	![image](https://user-images.githubusercontent.com/103415859/192133563-5bec007f-a3c0-4c34-9475-1345cc6f90b0.png)

	- Assumptions made:
		- housingType can only be `landed, condominium, hdb`


2.	Add Memember to Household

	- Route: `/household_add_member`
	- Type: `POST`
	- Form parameters: 
	 	- name (as a text box) - `name`
	 	- gender (as a dropdown list) - `male, female`
	 	- maritalStatus (as a dropdown list) - `married, single`
	 	- spouse (as a text box) - `spouse`
	 	- occupationType (as a dropdown list) - `unemployed, student, employed`
	 	- annualIncome (as a text box) - `annualIncome`
	 	- dob (as a Date calendar) - `dob`
	 	- household_id (as a text box) - `household_id`
	- `127.0.0:5000/addmember` or [Heroku](https://gov-grant.herokuapp.com/addmember)

	![image](https://user-images.githubusercontent.com/103415859/192134289-d49e46c4-b6e0-41c0-bf31-7dfbdc12cca0.png)

	- Assumptions made:
		- name cannot be empty
		- gender can only be `male, female`
		- meritalStatus can only be `married, single`
		- spouse can only be a positive number
		- members do not enter a spouse if they are single
		- when you are single, you cannot have a spouse
		- when you are married, you must have a spouse
		- you will have your spouse's id, automatically
		- your spouse will have your id, automatically
		- if you input a spouse, who is already taken, it wont be allowed
		- if you input a spouse, who already has another spouse, it wont be allowed
		- you and your spouse must be from the same household
		- occupationType can only be `unemployed, student, employed`
		- if annualIncome is left blank, it will be treated as 0
		- dob can only be `%Y, %m, %d`
		- dob must be entered
		- household_id can only be a positive number
		- household_id will be assumed to be the latest household created, if none is inputted


3. 	List All Households

	- Route: `/household_list_all`
	- Type: `GET`
	- Form parameters: 
	- `127.0.0:5000/listall` or [Heroku](https://gov-grant.herokuapp.com/listall)

	![image](https://user-images.githubusercontent.com/103415859/192136081-1ddfdb06-a1f0-4b26-bb28-06770d927b61.png)



4. 	Search Households

	- Route: `/household_search`
	- Type: `POST`
	- Form parameters: 
	 	- Household `id`
	- `127.0.0:5000/search` or [Heroku](https://gov-grant.herokuapp.com/search)

	![image](https://user-images.githubusercontent.com/103415859/192136218-6fc99ff2-df7a-4440-acaf-936f3909f20a.png)



5. 0	List Qualifying Households & Members

	- Route: `/household_list_qualifying`
	- Type: `GET`
	- Form parameters: 
	- `127.0.0:5000/listqaulifying` or [Heroku](https://gov-grant.herokuapp.com/listqaulifying)

	![image](https://user-images.githubusercontent.com/103415859/192136287-6c3849f0-4458-43a3-9a83-381883e74ca3.png)

	- Assumptions made:
		- There is another page for Student Encouragement Bonus, click the button.
		- There is another page for Multigeneration Scheme, click the button.
		- There is another page for Elder Bonus, click the button.
		- There is another page for Baby Sunshine Grant, click the button.
		- There is another page for YOLO GST Grant, click the button.



5. 1	List Qualifying Households & Members for SEB
	
	- Route: `/list_qualifying_modules/student_encouragement_bonus`
	- Type: `GET`
	- Form parameters: 
	- `127.0.0:5000/listqaulifying/SEB` or [Heroku](https://gov-grant.herokuapp.com/listqaulifying/SEB)

	![image](https://user-images.githubusercontent.com/103415859/192137111-7f87022e-3137-4fdb-b5bd-772dd296fe78.png)

	- Assumptions Made:
		- Following Criteria, the Qualifying Members with age < 16 years old, is a student. (Assuming Qualifying Members who fall under this bonus should be a student)



5. 2	List Qualifying Households & Members for MS
	
	- Route: `/list_qualifying_modules/multigeneration_scheme`
	- Type: `GET`
	- Form parameters: 
	- `127.0.0:5000/listqaulifying/MS` or [Heroku](https://gov-grant.herokuapp.com/listqaulifying/MS)

	![image](https://user-images.githubusercontent.com/103415859/192137122-e5ea598c-5eb5-4cf9-9784-59b5965e8e10.png)


	
5. 3	List Qualifying Households & Members for EB
	
	- Route: `/list_qualifying_modules/elder_bonus`
	- Type: `GET`
	- Form parameters: 
	- `127.0.0:5000/listqaulifying/EB` or [Heroku](https://gov-grant.herokuapp.com/listqaulifying/EB)

	![image](https://user-images.githubusercontent.com/103415859/192137228-8a483201-6391-4332-8cbc-14c59d5972df.png)

	- Assumptions Made:
		- Following Criteria, the Qualifying Members with age > 55 years old, is eligible. (Assuming Qualifying Members age => 55 is a typo)
	
	
	
5. 4	List Qualifying Households & Members for BSG
	
	- Route: `/list_qualifying_modules/baby_sunshine_grant`
	- Type: `GET`
	- Form parameters: 
	- `127.0.0:5000/listqaulifying/BSG` or [Heroku](https://gov-grant.herokuapp.com/listqaulifying/BSG)

	![image](https://user-images.githubusercontent.com/103415859/192137245-0f95055f-6539-4b13-963f-a0fc28a1bbe4.png)



5. 5	List Qualifying Households & Members for YGG
	
	- Route: `/list_qualifying_modules/yolo_gst_grant`
	- Type: `GET`
	- Form parameters: 
	- `127.0.0:5000/listqaulifying/YGG` or [Heroku](https://gov-grant.herokuapp.com/listqaulifying/YGG)

	![image](https://user-images.githubusercontent.com/103415859/192137276-9147915c-38b0-4f68-8e80-f58e500bd956.png)


## Initial Setup



	
## Thank You!

Admittedly as this was my first take home assignment, I have 
