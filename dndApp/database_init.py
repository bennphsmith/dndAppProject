'''
##############
DnD Database Initialisation File to create the database when first launching the Docker file
Author: Benjamin Smith
Last Edited: 17/04/2020
###############
'''

import json
import pprint
import urllib.request
from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1']) # Create new Cluster Instance and connect to Cassandra database
session = cluster.connect() # Create a new session

session.execute("CREATE KEYSPACE main WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1}") # Create new keyspace
session.set_keyspace('main') # Use keyspace for session

# Create user table
session.execute("""CREATE TABLE user(
                email text PRIMARY KEY, 
                first_name text, 
                last_name text, 
                password text)""")

# Create Character by User table
session.execute("""CREATE TABLE character_by_user(
                char_name text,
                char_align text,
                char_race text,
                char_class text,
                char_background text,
                char_desc text,
                char_lang list<text>,
                char_xp int,
                char_hp int,
                char_hp_temp int,
                char_armour int,
                char_speed int,
                char_int int,
                char_death int,
                char_ability map<text, int>,
                char_insp int,
                char_profbonus int,
                char_save map<text, int>,
                char_skill map<text, int>,
                char_perc int,
                char_prof text,
                char_equip text,
                char_features text,
                char_extra text,
                char_user text,
                PRIMARY KEY (char_name, char_user))""")

################Create Standard tables to call the dnd Attributes###############

######## Character Alignment Table
session.execute("""CREATE TABLE align(
                align_name text PRIMARY KEY,
                align_value text)""")

session.execute("INSERT INTO align(align_name, align_value) VALUES ('Lawful Good', 'lg')")
session.execute("INSERT INTO align(align_name, align_value) VALUES ('Neutral Good', 'ng')")
session.execute("INSERT INTO align(align_name, align_value) VALUES ('Chaotic Good', 'cg')")
session.execute("INSERT INTO align(align_name, align_value) VALUES ('Lawful Neutral', 'ln')")
session.execute("INSERT INTO align(align_name, align_value) VALUES ('Neutral', 'n')")
session.execute("INSERT INTO align(align_name, align_value) VALUES ('Chaotic Neutral', 'cn')")
session.execute("INSERT INTO align(align_name, align_value) VALUES ('Lawful Evil', 'le')")
session.execute("INSERT INTO align(align_name, align_value) VALUES ('Neutral Evil', 'ne')")
session.execute("INSERT INTO align(align_name, align_value) VALUES ('Chaotic Evil', 'ce')")


######### Create Background Table

session.execute("""CREATE TABLE background(
                background_name text PRIMARY KEY,
                background_value text)""")

session.execute("INSERT INTO background(background_name, background_value) VALUES ('Acolyte', 'acolyte')")
session.execute("INSERT INTO background(background_name, background_value) VALUES ('Charlatan', 'charlatan')")
session.execute("INSERT INTO background(background_name, background_value) VALUES ('Criminal', 'criminal')")
session.execute("INSERT INTO background(background_name, background_value) VALUES ('Entertainer', 'entertainer')")
session.execute("INSERT INTO background(background_name, background_value) VALUES ('Folk Hero', 'folk hero')")
session.execute("INSERT INTO background(background_name, background_value) VALUES ('Guild Artisan', 'guild artisan')")
session.execute("INSERT INTO background(background_name, background_value) VALUES ('Hermit', 'hermit')")
session.execute("INSERT INTO background(background_name, background_value) VALUES ('Noble', 'noble')")
session.execute("INSERT INTO background(background_name, background_value) VALUES ('Outlander', 'outlander')")
session.execute("INSERT INTO background(background_name, background_value) VALUES ('Sage', 'sage')")
session.execute("INSERT INTO background(background_name, background_value) VALUES ('Sailor', 'sailor')")
session.execute("INSERT INTO background(background_name, background_value) VALUES ('Soldier', 'soldier')")
session.execute("INSERT INTO background(background_name, background_value) VALUES ('Urchin', 'urchin')")