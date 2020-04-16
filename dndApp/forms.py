'''
##############
DnD Forms File to Create the forms for the website using WTForms
Author: Benjamin Smith
Last Edited: 15/04/2020
Forms Description:
1. RegistrationFrom - takes users details on registration page and provides relevant checks to database
2. LoginFrom - takes users details on login page and provides relevant checks to database
###############
'''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_cqlalchemy import CQLAlchemy
from dndApp.database import User


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

    # Checks database for user email to ensure they are a member and eligible to sign in
    def validate_email(self, email):
        AlreadyRegistered = False
        for user in User().all(): # Loop through all records in User
            if email.data == user.email: # Return boolean True if found
                AlreadyRegistered = True
        if AlreadyRegistered == False:
            raise ValidationError('Email address not registered!')
        else:
            return