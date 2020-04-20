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
9. CharDelete - deletes the character from the database
###############
'''

import requests
from flask import render_template, url_for, redirect, request
from dndApp import app, database, bcrypt
from dndApp.forms import RegistrationForm, LoginForm, CharacterForm
from dndApp.database import User, Character
from flask_bcrypt import Bcrypt
from flask_cqlalchemy import CQLAlchemy
from flask_login import login_user, logout_user, current_user, login_required

###################Registration, Login and Logout Pages######################

# Route to app main/registration page
@app.route('/', methods=['GET', 'POST']) # Multiple page routes
@app.route('/register/', methods=['GET', 'POST'])
def Register():
    if current_user.is_authenticated == True: # If user is logged in then redirect to library page
        return redirect(url_for('Library')), 200 # Succesful response but user is logged in already
    regForm = RegistrationForm() # Create form instance
    if (regForm.validate_on_submit() == True): # If form is submitted then ...
        hpass = bcrypt.generate_password_hash(
            regForm.password.data).decode('utf-8') # hash password and make into string
        user = User(
            email = regForm.email.data,
            first_name = regForm.first_name.data,
            last_name = regForm.last_name.data,
            password = hpass) # Create new instance of user
        user.save() # Save new user to database
        return redirect(url_for('Login')), 201 # User has been registered and now is needs to login to authenticate
    return render_template('register_form.html', form=regForm), 200

# Route to login page
@app.route('/login/', methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated == True: # If user is logged in redirect to library as there is no reason to login
        return redirect(url_for('Library'), 200) # Succesful response but user is logged in already
    logForm = LoginForm() # Create form instance
    if (logForm.validate_on_submit() == True):
        for user in User().all(): # Iterate through User database
            if (logForm.email.data == user.email) and (bcrypt.check_password_hash(user.password, logForm.password.data) == True):
                login_user(user) # Login user is email is in the database and password is correct
                return redirect(url_for('Library')), 200 
            else:
                redirect(url_for('Login')), 404 # If not in the database redirect to login page with 404 error
    return render_template('login_form.html', form=logForm), 200

# Route for Logout
@app.route('/logout/', methods=['GET'])
def Logout():
    logout_user()
    if current_user.is_active == False: # Check Logout status
        return redirect(url_for('Login')), 200 # Logout successful
    else:
        return redirect(url_for('Library')), 501 # Logut not implimented

###################External API Account Pages######################

# Route for Library (aka Home Page for a logged in User)
@app.route('/library/', methods=['GET'])
@login_required
def Library():
    # Below is an example status code return for if the user is not authenticated - 401
    # Login required handles this with a redirect to the login page - therefore is is not needed in all the routes
    if current_user.is_authenticated == True:
        return render_template('library.html'), 200 # Client able to access content
    else:
        return redirect(url_for('Login')), 401 # Client is unauthorized and therefore cannot view content

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
        redirect(url_for('Library')), 404 # External API resource no found
    return render_template('library_search.html', data=result), 200 # Data found and displayed okay

###################Character Account Pages######################

# Character Creation
@app.route('/create-character/', methods=['GET', 'POST'])
@login_required
def CharCreate():
    charForm = CharacterForm() # Create new instance of form
    if (charForm.validate_on_submit() == True): # If form is submitted then ...
        character = Character(
            # Input all the form data into the database using the ORM model
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
            char_ability = ({
                            'STR': charForm.char_absc_str.data, 
                            'DEX': charForm.char_absc_dex.data, 
                            'CON': charForm.char_absc_con.data, 
                            'INT': charForm.char_absc_int.data, 
                            'WIS': charForm.char_absc_wis.data, 
                            'CHA': charForm.char_absc_cha.data}),
            char_insp = charForm.char_insp.data,
            char_profbonus = charForm.char_profbonus.data,
            char_save = ({
                            'STR': charForm.char_save_str.data, 
                            'DEX': charForm.char_save_dex.data, 
                            'CON': charForm.char_save_con.data, 
                            'INT': charForm.char_save_int.data,
                            'WIS': charForm.char_save_wis.data, 
                            'CHA': charForm.char_save_cha.data}),
            char_skill = ({
                            'Acrobatics': charForm.char_skill_acro.data, 
                            'Animal-Handling': charForm.char_skill_anhan.data, 
                            'Arcana': charForm.char_skill_arc.data, 
                            'Athletics': charForm.char_skill_ath.data, 
                            'Deception': charForm.char_skill_dec.data, 
                            'History': charForm.char_skill_hist.data,
                            'Insight': charForm.char_skill_ins.data, 
                            'Intimidation': charForm.char_skill_int.data, 
                            'Investigation': charForm.char_skill_inv.data, 
                            'Medicine': charForm.char_skill_med.data, 
                            'Nature': charForm.char_skill_nat.data, 
                            'Perception': charForm.char_skill_perc.data,
                            'Performance': charForm.char_skill_perf.data, 
                            'Persuasion': charForm.char_skill_pers.data, 
                            'Religion': charForm.char_skill_rel.data, 
                            'Sleight of Hand': charForm.char_skill_sle.data, 
                            'Stealth': charForm.char_skill_ste.data, 
                            'Survival': charForm.char_skill_sur.data}),
            char_perc = charForm.char_perc.data,
            char_prof = charForm.char_prof.data,
            char_equip = charForm.char_equip.data,
            char_features = charForm.char_features.data,
            char_extra = charForm.char_extra.data,
            char_user = current_user.email) # Create new instance of using form inputs
        character.save() # Save new user to database
        return redirect(url_for('Library')), 201 # Character created successfully
    return render_template('character_from.html', form=charForm), 200

@app.route('/character-list', methods=['GET', 'POST'])
@login_required
def CharList():
    char_list = []
    for char in Character().all():
        if char.char_user == current_user.email: # Iterates through list of characters by user
            char_list.append(char.char_name) # Creates list of character names
    return render_template('character_list.html', char_list=char_list), 200

# Character Editing Page
@app.route('/edit-character/<character_name>', methods=['GET', 'POST'])
@login_required
def CharEdit(character_name):
    for char in Character().all():
        if char.char_name == character_name:
            character = char
    charForm = CharacterForm(obj=character) # Loads previous data into form 
    if (charForm.validate_on_submit() == True): # If form is submitted then ...
        character = Character(
            # Input all the form data into the database using the ORM model 
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
            # STILL TO DO - BELOW MAP NEEDS EXPLICITLY MAPPED TO FORM DATA FIELDS
            char_ability = {
                            'STR': charForm.char_absc_str.data, 
                            'DEX': charForm.char_absc_dex.data, 
                            'CON': charForm.char_absc_con.data, 
                            'INT': charForm.char_absc_int.data, 
                            'WIS': charForm.char_absc_wis.data, 
                            'CHA': charForm.char_absc_cha.data},
            char_insp = charForm.char_insp.data,
            char_profbonus = charForm.char_profbonus.data,
            char_save = {
                            'STR': charForm.char_save_str.data, 
                            'DEX': charForm.char_save_dex.data, 
                            'CON': charForm.char_save_con.data, 
                            'INT': charForm.char_save_int.data, 
                            'WIS': charForm.char_save_wis.data, 
                            'CHA': charForm.char_save_cha.data},
            char_skill = {
                            'Acrobatics': charForm.char_skill_acro.data, 
                            'Animal-Handling': charForm.char_skill_anhan.data, 
                            'Arcana': charForm.char_skill_arc.data, 
                            'Athletics': charForm.char_skill_ath.data, 
                            'Deception': charForm.char_skill_dec.data, 
                            'History': charForm.char_skill_hist.data,
                            'Insight': charForm.char_skill_ins.data, 
                            'Intimidation': charForm.char_skill_int.data, 
                            'Investigation': charForm.char_skill_inv.data, 
                            'Medicine': charForm.char_skill_med.data, 
                            'Nature': charForm.char_skill_nat.data, 
                            'Perception': charForm.char_skill_perc.data,
                            'Performance': charForm.char_skill_perf.data, 
                            'Persuasion': charForm.char_skill_pers.data, 
                            'Religion': charForm.char_skill_rel.data, 
                            'Sleight of Hand': charForm.char_skill_sle.data, 
                            'Stealth': charForm.char_skill_ste.data, 
                            'Survival': charForm.char_skill_sur.data},
            char_perc = charForm.char_perc.data,
            char_prof = charForm.char_prof.data,
            char_equip = charForm.char_equip.data,
            char_features = charForm.char_features.data,
            char_extra = charForm.char_extra.data,
            char_user = current_user.email) # Create new instance of character
        character.save() # Save new user to database
        return redirect(url_for('Library')), 201 # Database successfully updated
    return render_template('character_from.html', form=charForm), 200

@app.route('/delete-character/<character_name>', methods=['GET', 'DELETE'])
@login_required
def CharDelete(character_name):
    for char in Character().all():
        # Check character name and check user is authorised to delete character
        if char.char_name == character_name and char.char_user == current_user.email:
            char.delete()
            return render_template('character_list.html'), 204 # Character deleted successfully
    return render_template('character_list.html'), 404 # Object not found
