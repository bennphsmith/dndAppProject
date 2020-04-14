from cassandra.cluster import Cluster
from flask import Flask
from flask_cqlalchemy import CQLAlchemy

app = Flask(__name__)
app.config['CASSANDRA_HOSTS'] = ['127.0.0.1']
app.config['CASSANDRA_KEYSPACE'] = "main"
database = CQLAlchemy(app)

'''
session.execute("CREATE KEYSPACE main WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1}")
session.set_keyspace('main')

session.execute("CREATE TABLE user(email text PRIMARY KEY, first_name text, last_name text, password text)")

email = 'ben@ben.com'
first_name = 'ben'
last_name = 'smith'
password = 'password'
session.execute("INSERT INTO user(email, first_name, last_name, password) VALUES(%s, %s, %s, %s)", (email, first_name, last_name, password))


user = session.execute(
            "SELECT email FROM user WHERE (email=%s)", (email.data))

print(user)
'''

class User(database.Model):
    email = database.columns.Text(primary_key=True)
    first_name = database.columns.Text(required=True)
    last_name = database.columns.Text(required=True)
    password = database.columns.Text(required=True)


person = User(email = 'ben@s.com', first_name ='Blake', last_name='Eggleston', password = 'pass1')

person.save()
print(person.email)
print(person)
print(User().all())
email = 'ben@jimbo.com'
AlreadyRegistered = False
for user in User().all():
    print(user.email)
    if email == user.email:
        AlreadyRegistered = True

if AlreadyRegistered == True:
    print('Already Registered!')
else:
    print('Account Created!')