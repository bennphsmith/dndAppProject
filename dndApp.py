
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
from flask_cqlalchemy import CQLAlchemy

#Initialise app
app = Flask(__name__)
app.config['SECRET_KEY'] = '756ba24325dfc559acf36854910afc59' # Secret Key for security purposes (CSRF, {{form.hidden_tag()}})

##########Initialise Database#########
app.config['CASSANDRA_HOSTS'] = ['172.17.0.2:80']
app.config['CASSANDRA_KEYSPACE'] = "cqlengine"
database = CQLAlchemy(app)

#Set up User object as table
class User(database.Model):
    email = database.columns.Text(primary_key=True)
    first_name  = database.columns.Text()
    last_name = database.columns.Text()
    password - database.colums.Text()

    def __repr__(self):
        return (f'User {self.email}')

#########Create all app routes/pages##########
#Route to app main/registration page
@app.route('/', methods=['GET', 'POST'])
@app.route('/register/', methods=['GET', 'POST'])
def Register():
    regForm = RegistrationForm()
    if (regForm.validate_on_submit() == True):
        flash('Success', 'success')
        return redirect(url_for('Login'))
    return render_template('register_form.html', form=regForm)

#Route to login page
@app.route('/login/', methods=['GET', 'POST'])
def Login():
    logForm = LoginForm()
    return render_template('login_form.html', form=logForm)

######Common functions######




###########Run Script from Python##########
#Enable script to be run from python
if __name__ == "__main__":
    app.run(debug = True, port = 4000) #Allow dynamic changes with debugging enabled
