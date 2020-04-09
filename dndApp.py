
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

# Import necessary modules
# Flask for web server connectivity
# forms to use forms created in other directory file
from flask import Flask, render_template
from forms import RegistrationForm, LoginForm
# from forms import RegistrationForm, LoginForm

# Initialise app
app = Flask(__name__)
app.config['SECRET_KEY'] = '756ba24325dfc559acf36854910afc59' # Secret Key for security purposes (CSRF, {{form.hidden_tag()}})

# Route to app main/registration page
@app.route('/', methods=['GET', 'POST'])
@app.route('/register/', methods=['GET', 'POST'])
def Register():
    regForm = RegistrationForm()
    return render_template('register_form.html', form=regForm)

@app.route('/login/', methods=['GET', 'POST'])
def Login():
    logForm = LoginForm()
    return render_template('login_form.html', form=logForm)

#Enable script to be run from python
if __name__ == "__main__":
    app.run(debug = True, port = 4000) #Allow dynamic changes with debugging enabled
