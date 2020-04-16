'''
##############
DnD App File for App Routes
Author: Benjamin Smith
Last Edited: 15/04/2020
Routes Description:
1. Register - takes users to the Register page to sign up for an account and send details to database
2. Login - takes users to the Login page to sign into the account and access app content
3. Logout - logs users out of their current session
4. Library - takes users through to account page, has list of API request buttons for DnD information
5. LibResult - same library page although displays the results of the previous request
###############
'''

import requests
from flask import render_template, flash, url_for, redirect, request
from dndApp import app, database, bcrypt
from dndApp.forms import RegistrationForm, LoginForm
from dndApp.database import User
from flask_bcrypt import Bcrypt
from flask_cqlalchemy import CQLAlchemy
from flask_login import login_user, logout_user, current_user, login_required


# Route to app main/registration page
@app.route('/', methods=['GET', 'POST'])
@app.route('/register/', methods=['GET', 'POST'])
def Register():
    if current_user.is_authenticated: # If user is logged in then redirect to library page
        return redirect(url_for('Library'))
    regForm = RegistrationForm()
    if (regForm.validate_on_submit() == True): # If form is submitted then ...
        hpass = bcrypt.generate_password_hash(
            regForm.password.data).decode('utf-8') # hash password and make into string
        user = User(
            email = regForm.email.data,
            first_name = regForm.first_name.data,
            last_name = regForm.last_name.data,
            password = hpass 
            ) # Create new instance of user
        user.save() # Save new user to database
        flash('Success', 'success') #Display flash success message
        return redirect(url_for('Login'))
    return render_template('register_form.html', form=regForm)

# Route to login page
@app.route('/login/', methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('Library'))
    logForm = LoginForm()
    if (logForm.validate_on_submit() == True):
        for user in User().all(): # Iterate through User database
            if (logForm.email.data == user.email) and (bcrypt.check_password_hash(user.password, logForm.password.data) == True):
                login_user(user)
                return redirect(url_for('Library')) 
            else:
                redirect(url_for('Login'))
    return render_template('login_form.html', form=logForm)

# Route for Logout
@app.route('/logout/', methods=['GET'])
def Logout():
    logout_user()
    return redirect(url_for('Login'))

# Route for Library (aka Home Page for a logged in User)
@app.route('/library/', methods=['GET', 'POST'])
@login_required
def Library():
    print(current_user)
    return render_template('library.html')

# Route for Library page with search information posted
@app.route('/library/<index1>/<index2>/', methods=['GET', 'POST'])
#@login_required
def LibResult(index1, index2):
    dnd_url_template = 'http://dnd5eapi.co/api/{index1}/{index2}' # Create dynamic template for API call
    url = dnd_url_template.format(index1 = index1, index2 = index2) # Pass variables
    data = requests.get(url)
    if data.ok: # Check data recieved okay
        result = data.json()
    else:
        Print('An Error has occured!') # Pass back results to template
    return render_template('library_search.html', data=result)
