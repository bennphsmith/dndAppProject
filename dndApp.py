
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

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/about/', methods=['GET'])
def about():
    return render_template('original-true.html')

#Enable script to be run from python
if __name__ == "__main__":
    app.run(debug = True, port = 4000) #Allow dynamic changes with debugging enabled
