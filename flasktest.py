import mysql.connector
from flask import Flask, jsonify

try:
    mydb = mysql.connector.connect(host='localhost', user='root', password='alidev12345', database='mydb')
except:
    print('Error while connecting to MySQL!')

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/users')
def index():
    cursor = mydb.cursor()
    cursor.execute('select * from user')

    #get data and convert to json
    records = cursor.fetchall()
    fields = cursor.description
    columns = []
    for f in fields:
        columns.append(f[0])
    jsonData = []
    for r in records:
        data_dict = {}
        for i in range(len(columns)):
            data_dict[columns[i]] = r[i]
        jsonData.append(data_dict)
    return jsonify({'users': jsonData})
   
app.run()