import requests
import json
from flask import Flask, render_template, flash, url_for, redirect, jsonify
from pprint import pprint

app = Flask(__name__)
app.config['SECRET_KEY'] = '756ba24325dfc559acf36854910afc59' # Secret Key for security purposes: (CSRF, {{form.hidden_tag()}}) & Login

@app.route('/library/', methods=['GET', 'POST'])
def Library():
    return render_template('library.html')

@app.route('/library/<index1>/<index2>/', methods=['GET', 'POST'])
def LibResult(index1, index2):
    dnd_url_template = 'http://dnd5eapi.co/api/{index1}/{index2}'
    url = dnd_url_template.format(index1 = index1, index2 = index2)
    data = requests.get(url)
    if data.ok:
        result = data.json()
        #response = json.dumps(result.text, sort_keys = True, indent = 4, separators = (',', ': '))
    else:
        Print('An Error has occured!')
    return render_template('library_search.html', data=result)


@app.route('/library/strength/', methods=['GET', 'POST'])
def Strength():
    return ('<h1>Strength</h1>')

if __name__ == "__main__":
    app.run(debug = True, port = 4000) #Allow dynamic changes with debugging enabled