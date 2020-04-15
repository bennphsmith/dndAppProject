import requests
from flask import Flask, render_template, flash, url_for, redirect
from forms import SearchForm
from pprint import pprint


dnd_url_template = 'http://dnd5eapi.co/api/{index1}'
print(len(dnd_url_template))
print(index1)
index1 = 'skills'
print(len(dnd_url_template))
print(index1)
url = dnd_url_template.format(index1 = index1)
data = requests.get(url)

'''
if data.ok:
    search_result = data.json()
    pprint(search_result)
'''