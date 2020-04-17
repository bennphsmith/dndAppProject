import json
import pprint
import urllib.request
from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1']) # Create new Cluster Instance and connect to Cassandra database
session = cluster.connect() # Create a new session
session.set_keyspace('main') # Use keyspace for session

data_skills = json.load(urllib.request.urlopen('http://dnd5eapi.co/api/skills'))

session.execute("""CREATE TABLE skill(
                skill_name text PRIMARY KEY,
                skill_value text)""")

for obj in data_skills['results']:
    session.execute("""INSERT INTO skill(skill_name, skill_value) 
                    VALUES(%s, %s)""", 
                    (obj['name'], obj['index']))
