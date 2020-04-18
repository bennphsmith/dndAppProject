'''
##############
DnD App File for App Routes
Author: Benjamin Smith
Last Edited: 18/04/2020
Routes Description:
1. Register - takes users to the Register page to sign up for an account and send details to database
2. Login - takes users to the Login page to sign into the account and access app content
3. Logout - logs users out of their current session
4. Library - takes users through to account page, has list of API request buttons for DnD information
5. LibResult - same library page although displays the results of the previous request
6. CharCreate - takes users to Character Flaskform to to create a character and pass data to Cassandra
7. CharList - outputs the save characters and provides hyperlinks to go through to edit form page
8. CharEdit - edit character attributes throughout the campaign and updates them to the system on submit
###############
'''

import requests
from flask import render_template, flash, url_for, redirect, request
from dndApp import app, database, bcrypt
from dndApp.forms import RegistrationForm, LoginForm, CharacterForm
from dndApp.database import User, Character
from flask_bcrypt import Bcrypt
from flask_cqlalchemy import CQLAlchemy
from flask_login import login_user, logout_user, current_user, login_required

###################Registration, Login and Logout Pages######################

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
            password = hpass) # Create new instance of user
        user.save() # Save new user to database
        flash('Success', 'success') #Display flash success message
        return redirect(url_for('Login'))
    return render_template('register_form.html', form=regForm)

# Route to login page
@app.route('/login/', methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated: # If user is logged in redirect to library as there is no reason to login
        return redirect(url_for('Library'))
    logForm = LoginForm()
    if (logForm.validate_on_submit() == True):
        for user in User().all(): # Iterate through User database
            if (logForm.email.data == user.email) and (bcrypt.check_password_hash(user.password, logForm.password.data) == True):
                login_user(user) # Login user is email is in the database and password is correct
                return redirect(url_for('Library')) 
            else:
                redirect(url_for('Login')) # If not in the database redirect to login page
    return render_template('login_form.html', form=logForm)

# Route for Logout
@app.route('/logout/', methods=['GET'])
def Logout():
    logout_user()
    return redirect(url_for('Login'))

###################External API Account Pages######################

# Route for Library (aka Home Page for a logged in User)
@app.route('/library/', methods=['GET', 'POST']) #Possibly Get rid of POST Route!!!!!
@login_required
def Library():
    return render_template('library.html')

# Route for Library page with search information posted
@app.route('/library/<index1>/<index2>/', methods=['GET', 'POST'])
@login_required
def LibResult(index1, index2):
    dnd_url_template = 'http://dnd5eapi.co/api/{index1}/{index2}' # Create dynamic template for API call
    url = dnd_url_template.format(index1 = index1, index2 = index2) # Pass variables
    data = requests.get(url)
    if data.ok: # Check data recieved okay
        result = data.json()
    else:
        Print('An Error has occured!') # Pass back results to template
    return render_template('library_search.html', data=result)

###################Character Account Pages######################

# Character Creation
@app.route('/create-character/', methods=['GET', 'POST'])
@login_required
def CharCreate():
    charForm = CharacterForm() # Create new instance of form
    if (charForm.validate_on_submit() == True): # If form is submitted then ...
        character = Character(
            char_name = charForm.char_name.data,
            char_align = charForm.char_align.data,
            char_race = charForm.char_race.data,
            char_class = charForm.char_class.data,
            char_background = charForm.char_background.data,
            char_desc = charForm.char_desc.data,
            char_lang = charForm.char_lang.data,
            char_xp = charForm.char_xp.data,
            char_hp = charForm.char_hp.data,
            char_hp_temp = charForm.char_hp_temp.data,
            char_armour = charForm.char_armour.data,
            char_int = charForm.char_initiative.data,
            char_speed = charForm.char_speed.data,
            char_death = charForm.char_death.data,
            char_ability = {'STR': 1, 'CON': 2},
            char_insp = charForm.char_insp.data,
            char_profbonus = charForm.char_profbonus.data,
            char_save = {'STR': 1, 'CON': 2},
            char_skill = {'STR': 1, 'CON': 2},
            char_perc = charForm.char_perc.data,
            char_prof = charForm.char_prof.data,
            char_equip = charForm.char_equip.data,
            char_features = charForm.char_features.data,
            char_extra = charForm.char_extra.data,
            char_user = current_user.email) # Create new instance of using form inputs
        character.save() # Save new user to database
        flash('Success', 'success') #Display flash success message
        return redirect(url_for('Library'))
    return render_template('character_from.html', form=charForm)

@app.route('/character-list', methods=['GET', 'POST'])
@login_required
def CharList():
    char_list = []
    for char in Character().all():
        if char.char_user == current_user.email:
            char_list.append(char.char_name)
    return render_template('character_list.html', char_list=char_list)

# Character Creation
@app.route('/edit-character/<character_name>', methods=['GET', 'POST'])
@login_required
def CharEdit(character_name):
    for char in Character().all():
        if char.char_name == character_name:
            character = char
    charForm = CharacterForm(obj=character)
    if (charForm.validate_on_submit() == True): # If form is submitted then ...
        character = Character(
            char_name = charForm.char_name.data,
            char_align = charForm.char_align.data,
            char_race = charForm.char_race.data,
            char_class = charForm.char_class.data,
            char_background = charForm.char_background.data,
            char_desc = charForm.char_desc.data,
            char_lang = charForm.char_lang.data,
            char_xp = charForm.char_xp.data,
            char_hp = charForm.char_hp.data,
            char_hp_temp = charForm.char_hp_temp.data,
            char_armour = charForm.char_armour.data,
            char_int = charForm.char_initiative.data,
            char_speed = charForm.char_speed.data,
            char_death = charForm.char_death.data,
            char_ability = {'STR': 1, 'CON': 2},
            char_insp = charForm.char_insp.data,
            char_profbonus = charForm.char_profbonus.data,
            char_save = {'STR': 1, 'CON': 2},
            char_skill = {'STR': 1, 'CON': 2},
            char_perc = charForm.char_perc.data,
            char_prof = charForm.char_prof.data,
            char_equip = charForm.char_equip.data,
            char_features = charForm.char_features.data,
            char_extra = charForm.char_extra.data,
            char_user = current_user.email) # Create new instance of character
        character.save() # Save new user to database
        flash('Success', 'success') #Display flash success message
        return redirect(url_for('Library'))
    return render_template('character_from.html', form=charForm)
