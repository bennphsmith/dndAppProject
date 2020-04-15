
'''
##############
DnD App File
Author: Benjamin Smith
Last Edited: 01/04/2020
App Description:
1. Pull object data from: http://www.dnd5eapi.co/ and present it
2. Create login for users
3. Allow character creation and initialisation
4. Allow editing of character through adventure with API
###############
'''

#########Initialise and Configure App and Import Modules############
# Flask for web server connectivity
# forms to use forms.py in same directory
import requests
from flask import Flask, render_template, flash, url_for, redirect
from forms import RegistrationForm, LoginForm, SearchForm
from cassandra.cluster import Cluster
from flask_bcrypt import Bcrypt
from flask_cqlalchemy import CQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

#Initialise app
app = Flask(__name__)
app.config['SECRET_KEY'] = '756ba24325dfc559acf36854910afc59' # Secret Key for security purposes: (CSRF, {{form.hidden_tag()}}) & Login
bcrypt = Bcrypt(app) # Initialise hashing framework


#############Initialise Login Manager#############
login_manager = LoginManager(app) # Create Login Manager Instances

# Define Load User function
@login_manager.user_loader
def load_user(user_id):
    for user in User().all():
        if user_id == user.email:
            return user


##########Initialise Database#########
app.config['CASSANDRA_HOSTS'] = ['127.0.0.1'] # Set database location
app.config['CASSANDRA_KEYSPACE'] = "main" # Set database keyspace
database = CQLAlchemy(app) # Create instance of CQLAlchemy database for app


#########Create all app routes/pages##########
# Route to app main/registration page
@app.route('/', methods=['GET', 'POST'])
@app.route('/register/', methods=['GET', 'POST'])
def Register():
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    regForm = RegistrationForm()
    if (regForm.validate_on_submit() == True): # If for is submitted then ...
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
    logForm = LoginForm()
    if (logForm.validate_on_submit() == True):
        for user in User().all(): # Iterate through User database
            if logForm.email.data == user.email:
                logUser = user # Store details for user
                hashpass = user.password
        if bcrypt.check_password_hash(hashpass, logForm.password.data): # Perfomed hashed password check, if accepted then redirect to home page and login
            login_user(logUser)
            return redirect(url_for('Home'))
        else:
            return redirect(url_for('Login')) # If login page unsucessful return user to login page
    return render_template('login_form.html', form=logForm)

# Route for Logout
@app.route('/logout/', methods=['GET'])
def Logout():
    logout_user()
    return ('<h1>You are Logged out</h1>')

# Route to home page for user
@app.route('/home/', methods=['GET', 'POST'])
def Home():
    dnd_url_template = 'http://dnd5eapi.co/api/'
    searchForm = SearchForm()
    if (searchForm.validate_on_submit() == True):
        search_data = 
    return ('<h1>Hello World!</h1>')



######Common functions######

##########Database#############

# Create and Initialise User Class
class User(database.Model, UserMixin):
    email = database.columns.Text(primary_key=True) # Make email primary key
    first_name = database.columns.Text(required=True)
    last_name = database.columns.Text(required=True)
    password = database.columns.Text(required=True)

    # Override get_id method in login_mangager class as email is used instead of 'id'
    def get_id(self):
        try:
            return str(User.email) # String needs to be returned
        except AttributeError:
            raise NotImplementedError('Still not working')

###########Run Script from Python##########
#Enable script to be run from python
if __name__ == "__main__":
    app.run(debug = True, port = 4000) #Allow dynamic changes with debugging enabled
