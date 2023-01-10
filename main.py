import mysql.connector
from flask import Flask, jsonify, request, session

try:
    mydb = mysql.connector.connect(host='localhost', user='root', password='alidev12345', database='mydb')
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
        if session['role'] == 'superuser':
            cursor.execute('select name, email, address, phone, birthdate, role from user')
            #get data and convert to json
            records = cursor.fetchall()
            return jsonify({'users': records})
        else:
            return jsonify({'message': 'Only admins can see users info!'})

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
    
@app.route('/logout', methods=['GET'])
def logout():
    if 'logged' in session.keys() and session['logged']:
        session['logged'] = False
        return jsonify({'message': 'Logged out successfully!'})
    else:
        return jsonify({'message': 'You are already logged out!'})
    
@app.route('/three-worst-comments', methods=['GET'])
def threeworstcomments():
    pname = request.args.get('pname')
    cursor.execute('SELECT user.name, comment.text, comment.date, comment.rate FROM comment, user where comment.Customer_user_id = user.id and comment.Product_name = %s order by comment.rate limit 3', (pname,))
    comments = cursor.fetchall()
    return jsonify({'comments': comments})

@app.route('/supplier-city', methods=['GET'])
def suppliercity():
    city = request.args.get('city')
    cursor.execute('SELECT * FROM supplier where address like %s', ("%{}%".format(city),))
    suppliers = cursor.fetchall()
    return jsonify({'suppliers': suppliers})



app.run(debug=True)