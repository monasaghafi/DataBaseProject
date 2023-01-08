import mysql.connector
from flask import Flask, jsonify, request, session

try:
    mydb = mysql.connector.connect(host='localhost', user='root', password='9718', database='mydb')
    cursor = mydb.cursor(dictionary=True)
except:
    print('Error while connecting to MySQL!')

app = Flask(__name__)
app.secret_key = '4lid3v5ecr3t'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/users')
def getUsers():
    if 'logged' not in session.keys() or not session['logged']:
        return jsonify({'message': 'You have to login first!'})
    else:
        cursor.execute('select name, email, address, phone, birthdate, role from user')
        #get data and convert to json
        records = cursor.fetchall()
        return jsonify({'users': records})

@app.route('/register', methods=['GET'])
def register():
    username = request.args.get('username')
    password = request.args.get('password')
    address = request.args.get('address')
    phone = request.args.get('phone')
    email = request.args.get('email')
    bdate = request.args.get('bdate')
    role = 'user'
    cursor.execute('SELECT * FROM user WHERE name = %s', (username,))
    user = cursor.fetchone()
    if user:
        return jsonify({'message': 'This username is already exists!'})
    cursor.execute('INSERT INTO user (password, name, address, phone, email, birthdate, role) VALUES (%s, %s, %s, %s, %s, %s, %s)', (password, username, address, phone, email, bdate, role))
    mydb.commit()
    return jsonify({'message': 'user registered successfully!'})

@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    cursor.execute('SELECT * FROM user WHERE name = %s and password = %s', (username, password))
    user = cursor.fetchone()
    if user:
        session['logged'] = True
        session['userid'] = user['id']
        session['username'] = user['name']
        session['role'] = user['role']
        print(session)
        return jsonify({'message': 'Logged in successfully!'})
    else:
        return jsonify({'message': 'username or password is incorrect!'})

@app.route('/categories', methods=['GET'])
def getCategory():
    #select distinct category from product
    cursor.execute('select distinct category from product')
    category = cursor.fetchall()
    return jsonify({'category': category})


app.run(debug=True)