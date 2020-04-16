'''
##############
DnD App File for Database Models
Author: Benjamin Smith
Last Edited: 15/04/2020
database Description:
1. User - Creates User model for CQLAlchemy to perform ORM functions with Cassandra
###############
'''

from flask_cqlalchemy import CQLAlchemy
from flask_login import UserMixin
from dndApp import database, login

# Define Load User function
@login.user_loader
def load_user(id):
    for user in User().all():
        if id == user.email:
            return user

# Create and Initialise User Class
class User(database.Model, UserMixin):
    email = database.columns.Text(primary_key=True) # Make email primary key
    first_name = database.columns.Text(required=True)
    last_name = database.columns.Text(required=True)
    password = database.columns.Text(required=True)

    
    # Override get_id method in login_mangager class as email is used instead of 'id'
    def get_id(self):
        return self.email # String needs to be returned
    