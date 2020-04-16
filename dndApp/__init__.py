'''
##############
DnD App File for Initialisation
Author: Benjamin Smith
Last Edited: 15/04/2020
App Description:
1. Take Users to Registration Page to Sign up to App service
2. Save details in Cassandra Cloud Database and call them to Login
3. Sent User through to Library Page where they can make dynamic requests to external API:
    http://www.dnd5eapi.co/
4. Allow users to create Characters which are then saved to the database
5. Users can check character creations and edit them throughout the campaign
###############
'''

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cqlalchemy import CQLAlchemy


# Initialise app
app = Flask(__name__)
app.config['SECRET_KEY'] = '756ba24325dfc559acf36854910afc59' # Secret Key for security purposes: (CSRF, {{form.hidden_tag()}}) & Login
app.config['CASSANDRA_HOSTS'] = ['127.0.0.1']
app.config['CASSANDRA_KEYSPACE'] = "main" # Set database keyspace
bcrypt = Bcrypt(app) # Initialise hashing framework
login = LoginManager(app) # Create Login Manager Instances
login.login_view = 'Login'
database = CQLAlchemy(app) # Create instance of CQLAlchemy database for app

from dndApp import routes