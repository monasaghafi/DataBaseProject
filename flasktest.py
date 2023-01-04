import json

import mysql.connector
from flask import Flask

try:
    mydb = mysql.connector.connect(host='localhost', user='root', password='alidev12345', database='mydb')
except:
    print('Error while connecting to MySQL!')

app = Flask(__name__)
@app.route('/users')
def index():
    cursor = mydb.cursor()
    cursor.execute('select * from user')
    records = cursor.fetchall()
    data = []
    for r in records:
        d = {}
        d['id'] = r[0]
        d['name'] = r[1]
        d['password'] = r[2]
        d['address'] = r[3]
        d['phone'] = r[4]
        d['email'] = r[5]
        d['birthdate'] = str(r[6])
        d['role'] = r[7]
        data.append(d)
    return json.dumps(data)    
   
app.run()