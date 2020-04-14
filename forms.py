'''#####################
Forms classes for registering new users and logging current users
Including methods for authenticating email
Author: Benjamin Smith
Last Edit: 09/04/2020
#####################'''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from cassandra.cluster import Cluster
from flask_cqlalchemy import CQLAlchemy

# Create Registration From for user
# Username takes the for of an email with is inherently unique (primary key)
# Password must be between 2 & 20 characters
# Confirm password checks that user entered the intended password
class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # Check if email address is already contained in the system
    # Display error message on the form if email address is already in use
    # Validator automatically called when email field submitted
    def validate_email(self, email):
        AlreadyRegistered = False
        for user in User().all(): # Loop through all records in User
            if email.data == user.email: # Return boolean True if found
                AlreadyRegistered = True
        if AlreadyRegistered == True:
            raise ValidationError('Email address already registered!')
        else:
            return


# Create Login Form for user
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Login')

    def validate_email(self, email):
        AlreadyRegistered = False
        for user in User().all(): # Loop through all records in User
            if email.data == user.email: # Return boolean True if found
                AlreadyRegistered = True
        if AlreadyRegistered == False:
            raise ValidationError('Email address not registered!')
        else:
            return


        cluster = Cluster(['127.0.0.1']) #Initialise Cluster
        session = cluster.connect('main') #Connect to keyspace
        users_list = session.execute(
            "SELECT * FROM user WHERE email = %s", [email.data]) #Return tuples where email address is same as one entered
        try:
            user = users_list[0] #Get single tuple
        except IndexError:
            raise ValidationError('Email address not registered!')
        else:
            return
    '''    
    def validate_password(self, password):
        cluster = Cluster(['127.0.0.1']) #Initialise Cluster
        session = cluster.connect('main') #Connect to keyspace
    '''

# Import at the bottom to prevent circular import error with the database - need to make files into better package structure
from dndApp import database, User
