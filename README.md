Simon Hagerup Jensen - MTH430, 
Christer Kold Lindholm - TRH104,
Christian Max Torp-Christensen - HNS484


# GreatGames

## Installation ★
(1) Clone the git repository and run requirements.txt to install required packages.

    pip install -r requirements.txt 

(2) Create a new database in pgAdmin 4 named GreatGames. 

(3) Configure the .env file with your pgAdmin variables:

    SECRET_KEY=<secret_key>
    DB_USERNAME=postgres || <postgres_user_name>
    DB_PASSWORD=<postgres_user_password>
    DB_NAME=GreenGroceries || <postgres_db_name>

(4) In the utils folder, run init_db.py to build the database by executing users.sql and games.sql.

ALTERNATIVE: In the utils folder, run both users.sql and games.sql with psql. Example:

    psql -h localhost -p 5432 -U postgres -d GreatGames -f users.sql 

(5) Go to the root folder and start the project in development mode using

    flask run 

or (depending on your PATH) with

    py -m flask run

then access the protoype webpage. 

## Guide ★★

### Searching the database 
- We generated an entirely new database containing 10,000 games with various attributes.
- The All Games page contains various SQL queries to the database.

### Regex
The Description field under All Games will use either SQL regex or Python regex to search through descriptions.

Searching for any string similar to "age 10", "AGe 10" will pattern match and only show games with the description containing "Age Restriction: 10".

When not searching for age, SQL uses normal Regex pattern matching.

### Logging in and adding games to the database
- You can log in to the website with username "developer" and password "pass".
- You can create your own customer profile.

## Development comments ★★★
- Developers cannot add new games, only replicas of existing titles. Games are digital rights and should not have quantity. Developers should be able to add entirely new games.


## Folder setup 📁

The app is divided into multiple folders similar to the structure of the example project, with a few tweaks:

- __blueprints__: Contains all the separate blueprints of the app (submodules of the app the store different parts of the functionality)
- __dataset__: Contains the csv file used to import the produce data
- __static__: Contains static files like images, css and js files (in this case javascript was not needed in the frontend)
- __templates__: This is the template folder of the app that stores all html files that are displayed in the user browser.
- __utils__: Contains the sql files and script that generate the postgresql database. Also contains a script that generates custom choices objects for flask forms used in SelectFields taken from the dataset.

At the root folder of the app (./GreenGroceries) six more scripts are present with the following roles:

- __\_\_init\_\_.py__: Initializes the flask app and creates a connection to the database (and a cursor object for future queries)
- __app.py__: Runs the app created by \_\_init__.py
- __filters.py__: Implements custom template filters for nicer formatting of data in the frontend
- __forms.py__: Implements forms used to save data from users (similar to the example project)
- __models.py__: Implements custom classes for each of the database tables to store data in a clean OOP manner (again, similar to the example project, but our models inherit the dict class for faster and more readable lookups)
- __queries.py__: Implements functions for each needed query to the database used inside the app (similar to the functional part of the models.py file within the example project)

## Routes 📌

Both implemented blueprints come with a __routes.py__ file that initialize a __Blueprint__ object and define _routes_
for the app.

- __Login__:
    - __/home__: Home page
    - __/about__: About page
    - __/style-guide__: Style guide (displays all html elements used, just for fun and css debugging)
    - __/login__: User login page (for simplicity in debugging, password hashing was omitted even though the example project made it pretty clear and easy to implement with bcrypt)
    - __/signup__: User signup (creation) page
    - __/logout__: Logs user out and sends back to login page

- __Produce__:
    - __/produce__: Search page for all produce in the database
    - __/add-produce__: Page where farmer users can add their produce (customers trying to submit will get an error)
    - __/your-produce__: Page where farmers can view and manage their produce
    - __/produce/restock/<pk>__: Page where farmers can restock a certain product
    - __/produce/buy/<pk>__: Page where customers get redirected to in order to buy a certain product
    - __/produce/your-orders__: Page where customers can view their orders

## Known backend issues / Intended features ⁉

- There is no good differentiation between customers and farmers in the _current_user_ global variable
- This results in some security issues when accessing links ment for farmers as customers and vice-versa (should be
  checked by the validation methods of the forms, but in the perfect scenario specific links should only be accessible
  by specific users)
- Given the correct url, developers may be able to update data on other developers produce (not tested, but seems logical)