#######################################################
DnD Cloud Application
Author: Benjamin Smith
Last edit: 09/04/2020
QM ECS781P Coursework - Cloud Computing
######################################################~

#########Description##########  
This app helps save and manage charcters during a dnd Campaign and contains the following functionalities:

- Register: Signs up users using FlaskForm for inputs. Delivers the user details to Cassandra database where they can be authenticated to access the content
(CQLAlchemy is used as an ORM to map database objects to Object Oriented models in code)
- Login: Authenticates users based on a hashed password call to the database. Used Flask-Login frawework to initiate a user session and check authentication
- Library: Allows user and interface to make external API calls to http://www.dnd5eapi.co, where the json data is retreived and displayed on the page
- Character Create: Character is created passing inputs using FlaskForm, where details are save in the database
- Charatcer List: List of created characters are displayed for the current user, where they can be edited or deleted


#########Frameworks##########
Docker - v: 19.03.8
Python - v: 3.6.9
Flask - v: 1.1.1
Cassandra - docker - cassandra:latest:
Bootstrap
pip3 install WTF-Flask (WTForms)
pip3 install flask-cqlalchmey
pip3 install flask-login


#########Instructions##########
Cassandra Database should be initialised using Docker command:

'docker run -d -p 9042:9042 --name dnd_database cassandra:latest'

Once docker container is running, the database can be initialised using:

'python3 database_init.py'

This sets up the database using cassandra.cluster commands in a python script

The app can now be run by using:

'python3 run.py'

#########Directories##########

dndApp - Contains all files related to the App along with __init__ file for config
templates - Contains all the templates used to render the webpages in HTML
Archive - Contains previous iterations of the code when building the App

Further details can be found at the head of each file

