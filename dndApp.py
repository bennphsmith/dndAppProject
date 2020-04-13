
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
#Flask for web server connectivity
#forms to use forms.py in same directory
from flask import Flask, render_template, flash, url_for, redirect
from forms import RegistrationForm, LoginForm
from cassandra.cluster import Cluster
from flask_bcrypt import Bcrypt

#Initialise app
app = Flask(__name__)
app.config['SECRET_KEY'] = '756ba24325dfc559acf36854910afc59' # Secret Key for security purposes (CSRF, {{form.hidden_tag()}})
bcrypt = Bcrypt(app) #Initialise hashing framework

##########Initialise Database#########
cluster = Cluster(['127.0.0.1']) #Set up cluster and map to local machine
session = cluster.connect() #Connect to cluster
session.set_keyspace('main')


#########Create all app routes/pages##########
#Route to app main/registration page
@app.route('/', methods=['GET', 'POST'])
@app.route('/register/', methods=['GET', 'POST'])
def Register():
    regForm = RegistrationForm()
    if (regForm.validate_on_submit() == True):
        hpass = bcrypt.generate_password_hash(regForm.password.data).decode('utf-8') #hash password and make into string
        session.execute(
            "INSERT INTO user(email, first_name, last_name, password) VALUES(%s, %s, %s, %s)", 
            (regForm.email.data, regForm.first_name.data, regForm.last_name.data, hpass)) #Pass data to Cass Database
        flash('Success', 'success') #Display flash success message
        return redirect(url_for('Login'))
    return render_template('register_form.html', form=regForm)

#Route to login page
@app.route('/login/', methods=['GET', 'POST'])
def Login():
    logForm = LoginForm()
    if (logForm.validate_on_submit() == True):
        return redirect(url_for('Home'))
    return render_template('login_form.html', form=logForm)

######Common functions######
@app.route('/home/', methods=['GET', 'POST'])
def Home():
    return ('<h1>Hello World!</h1>')




###########Run Script from Python##########
#Enable script to be run from python
if __name__ == "__main__":
    app.run(debug = True, port = 4000) #Allow dynamic changes with debugging enabled
