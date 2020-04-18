'''
##############
DnD Forms File to Create the forms for the website using WTForms
Author: Benjamin Smith
Last Edited: 15/04/2020
Forms Description:
1. RegistrationFrom - takes users details on registration page and provides relevant checks to database
2. LoginFrom - takes users details on login page and provides relevant checks to database
3. CharacterForm - takes details on Character Creation and provides relevant checks
###############
'''

import json
import urllib.request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_cqlalchemy import CQLAlchemy
from dndApp.database import User, Character, Align, Background


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

# Get Request to external API to get the data for the SelectField Lists
data_class = json.load(urllib.request.urlopen('http://dnd5eapi.co/api/classes')) # Transform data into dictionary for ease of access
data_language = json.load(urllib.request.urlopen('http://dnd5eapi.co/api/languages'))
data_races = json.load(urllib.request.urlopen('http://dnd5eapi.co/api/races'))

class CharacterForm(FlaskForm):
    char_name = StringField('Name', validators=[DataRequired()])
    char_align = SelectField(u'Alignment', validators=[DataRequired()], choices=[(align.align_value, align.align_name) for align in Align().all()])
    char_race = SelectField(u'Race', validators=[DataRequired()], choices=[(race['index'], race['name']) for race in data_races['results']])
    char_class = SelectField(u'Class', validators=[DataRequired()], choices=[(charClass['index'], charClass['name']) for charClass in data_class['results']])
    char_background = SelectField('Background', validators=[DataRequired()], choices=[(background.background_value, background.background_name) for background in Background().all()])
    char_desc = TextAreaField('Description')
    char_lang = SelectMultipleField(u'Languages', choices=[(lang['index'], lang['name']) for lang in data_language['results']])
    char_xp = IntegerField('XP', validators=[DataRequired()], default=0) # Start on 0
    char_hp = IntegerField('HP', validators=[DataRequired()])
    char_hp_temp = IntegerField('Temporary HP', default=0) # Start on 0
    char_armour = IntegerField('Armour Class', validators=[DataRequired()])
    char_initiative = IntegerField('Initiative', validators=[DataRequired()]) # Also the dex modifier
    char_speed = IntegerField('Speed', validators=[DataRequired()], default=25)
    char_death = IntegerField('Death Throws', default=0) # Start on 0
    # List all the ability scores for the form
    char_absc_str = IntegerField('STR', validators=[DataRequired()]) # List with ability scorce and modifier per trait, modifier based on score
    char_absc_dex = IntegerField('DEX', validators=[DataRequired()])
    char_absc_con = IntegerField('CON', validators=[DataRequired()])
    char_absc_int = IntegerField('INT', validators=[DataRequired()])
    char_absc_wis = IntegerField('WIS', validators=[DataRequired()])
    char_absc_cha = IntegerField('CHA', validators=[DataRequired()])
    char_insp = IntegerField('Inspriation', validators=[DataRequired()], default=0) # Start with 0
    char_profbonus = IntegerField('Proficiency Bonus', validators=[DataRequired()], default=0) # Start with 0 but increase proportional to level
    # List all saving throws - enter manually as this can change depending on the character
    char_save_str = IntegerField('STR', validators=[DataRequired()]) # List with ability scorce and modifier per trait, modifier based on score
    char_save_dex = IntegerField('DEX', validators=[DataRequired()])
    char_save_con = IntegerField('CON', validators=[DataRequired()])
    char_save_int = IntegerField('INT', validators=[DataRequired()])
    char_save_wis = IntegerField('WIS', validators=[DataRequired()])
    char_save_cha = IntegerField('CHA', validators=[DataRequired()])
    # List all skill modifiers
    char_skill_arco = IntegerField('Acrobatics', validators=[DataRequired()])
    char_skill_anhan = IntegerField('Animal Handling', validators=[DataRequired()])
    char_skill_arc = IntegerField('Arcana', validators=[DataRequired()])
    char_skill_ath = IntegerField('Athletics', validators=[DataRequired()])
    char_skill_dec = IntegerField('Deception', validators=[DataRequired()])
    char_skill_hist = IntegerField('History', validators=[DataRequired()])
    char_skill_ins = IntegerField('Insight', validators=[DataRequired()])
    char_skill_int = IntegerField('Intimidation', validators=[DataRequired()])
    char_skill_inv = IntegerField('Investigation', validators=[DataRequired()])
    char_skill_med = IntegerField('Medicine', validators=[DataRequired()])
    char_skill_nat = IntegerField('Nature', validators=[DataRequired()])
    char_skill_perc = IntegerField('Perception', validators=[DataRequired()])
    char_skill_perf = IntegerField('Performance', validators=[DataRequired()])
    char_skill_pers = IntegerField('Persuasion', validators=[DataRequired()])
    char_skill_rel = IntegerField('Religion', validators=[DataRequired()])
    char_skill_sle = IntegerField('Sleight of Hand', validators=[DataRequired()])
    char_skill_ste = IntegerField('Stealth', validators=[DataRequired()])
    char_skill_sur = IntegerField('Survival', validators=[DataRequired()])
    ###########
    char_perc = IntegerField('Perception', validators=[DataRequired()]) # 10 + perception bonus
    char_prof = TextAreaField('Proficiencies') # Big Text box for them to enter details manually how they like
    char_equip = TextAreaField('Equipment') # Big Text box for them to enter details manually how they like
    char_features = TextAreaField('Features') # Big Text box for them to enter details manually how they like
    char_extra = TextAreaField('Extra Information') # Big Text box for them to enter details manually how they like, meant to include: traits, ideals, bonds and flaws
    submit = SubmitField('Create Character')

    # Check that the character name is not already taken
    def validate_email(self, name):
        AlreadyCreated = False
        for char in Character_by_user().all(): # Loop through all records in User
            if name.data == char.email: # Return boolean True if found
                AlreadyRegistered = True
        if AlreadyRegistered == True:
            raise ValidationError('You already have this character name')
        else:
            return