import csv

# API created by Mitchell Zarb | Y12
import sqlite3
import json
sql_command = "select Superhero ID, Superhero Name, image from superhero;"
with sqlite3.connect("/Users/hunterbarrett/Documents/GitHub/IA2-Hunter-Barrett/superherodatabase.db") as database:
    cursor = database.cursor()
    cursor.execute(sql_command)
results = cursor.fetchall()

print (json.dumps(results))