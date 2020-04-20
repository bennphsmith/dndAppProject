'''
##############
DnD App File for Database Models
Author: Benjamin Smith
Last Edited: 20/04/2020
database Description:
1. User - Creates User model for CQLAlchemy to perform ORM functions with Cassandra
2. Character - Creates Character model for CQLAlchemy to perform ORM functions with Cassandra
3. Align - creates a list of values for Alignment
4. Background - creates list of valuses for Background attribute
###############
'''

from flask_cqlalchemy import CQLAlchemy
from flask_login import UserMixin
from dndApp import database, login

# Define Load User function for login - required to keep user in session
@login.user_loader
def load_user(id):
    for user in User().all():
        if id == user.email:
            return user

###################Account Classes#################
# Create User Class
class User(database.Model, UserMixin):
    email = database.columns.Text(primary_key=True) # Make email primary key
    first_name = database.columns.Text(required=True)
    last_name = database.columns.Text(required=True)
    password = database.columns.Text(required=True)

    
    # Override get_id method in login_mangager class as email is used instead of 'id'
    def get_id(self):
        return self.email # String needs to be returned

# Create Character Class
class Character(database.Model):
    __table_name__ = 'character_by_user' # Map to database table name
    char_name = database.columns.Text(primary_key=True)
    char_align = database.columns.Text(required=True)
    char_race = database.columns.Text(required=True)
    char_class = database.columns.Text(required=True)
    char_background = database.columns.Text(required=True)
    char_desc = database.columns.Text()
    char_lang = database.columns.List(database.columns.Text)
    char_xp = database.columns.Integer() # Start on 0
    char_hp = database.columns.Integer(required=True)
    char_hp_temp = database.columns.Integer() # Start on 0
    char_armour = database.columns.Integer(required=True)
    char_int = database.columns.Integer(required=True) # Also the dex modifier
    char_speed = database.columns.Integer(required=True)
    char_death = database.columns.Integer() # Start on 0 (can go 1 - 3, on 3 is deleted)
    char_ability = database.columns.Map(database.columns.Text, database.columns.Integer, required=True) # Map UserType ability scores to traits
    char_insp = database.columns.Integer() # Start with 0
    char_profbonus = database.columns.Integer(required=True) # Start with 0 but increase proportional to level
    char_save = database.columns.Map(database.columns.Text, database.columns.Integer, required=True) # List with saving throw per trait
    char_skill = database.columns.Map(database.columns.Text, database.columns.Integer, required=True) # List with skill modifier per skill
    char_perc = database.columns.Integer(required=True) # 10 + perception bonus
    char_prof = database.columns.Text() # Big Text box for them to enter details manually how they like
    char_equip = database.columns.Text() # Big Text box for them to enter details manually how they like
    char_features = database.columns.Text() # Big Text box for them to enter details manually how they like
    char_extra = database.columns.Text() # Big Text box for them to enter details manually how they like, meant to include: traits, ideals, bonds and flaws
    char_user = database.columns.Text(required=True) # Denotes the charcter creator user, should be used as the partition key

#################Character Creation Database Lists#################
##############List of attributes needed but not found in the external API
##############Created in the database for consistency and ease of access

class Align(database.Model):
    align_name = database.columns.Text(primary_key=True)
    align_value = database.columns.Text(required=True)

class Background(database.Model):
    background_name = database.columns.Text(primary_key=True)
    background_value = database.columns.Text(required=True)