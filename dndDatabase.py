from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1']) #Set up cluster and map to local machine
session = cluster.connect() #Connect to cluster

session.execute("CREATE KEYSPACE main WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1}")
session.set_keyspace('main')

session.execute("CREATE TABLE user(email text PRIMARY KEY, first_name text, last_name text, password text)")
'''
email = 'ben@ben.com'
first_name = 'ben'
last_name = 'smith'
password = 'password'
session.execute("INSERT INTO user(email, first_name, last_name, password) VALUES(%s, %s, %s, %s)", (email, first_name, last_name, password))
'''