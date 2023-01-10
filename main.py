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
    
@app.route('/edit-profile', methods=['GET'])
def editprofile():
    if 'logged' in session.keys() and session['logged']:
        try:
            password = request.args.get('password', default=None, type=str)
            name = request.args.get('username', default=None, type=str)
            address = request.args.get('address', default=None, type=str)
            phone = request.args.get('phone', default=None, type=str)
            email = request.args.get('email', default=None, type=str)
            birthdate = request.args.get('birthdate', default=None, type=str)
            query = 'UPDATE user SET '
            is_first = True
            if password is not None:
                query += ('password = "' + password + '"') if is_first else (', password = "' + password + '"')
                is_first = False
            if name is not None:
                query += ('name = "' + name + '"') if is_first else (', name = "' + name + '"')
                is_first = False
            if address is not None:
                query += ('address = "' + address + '"') if is_first else (', address = "' + address + '"')
                is_first = False
            if phone is not None:
                query += ('phone = "' + phone + '"') if is_first else (', phone = "' + phone + '"')
                is_first = False
            if email is not None:
                query += ('email = "' + email + '"') if is_first else (', email = "' + email + '"')
                is_first = False
            if birthdate is not None:
                query += ('birthdate = "' + birthdate + '"') if is_first else (', birthdate = "' + birthdate + '"')
                is_first = False
            query += ' WHERE id = "' + str(session['userid']) + '"'
            cursor.execute(query)
            mydb.commit()
        except:
            return jsonify({'message': 'Please enter correct info!'})
        return jsonify({'message': 'Your info edited successfully!'})
    else:
        return jsonify({'message': 'You have to login first!'})
    
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

@app.route('/most-product-last-month', methods=['GET'])
def lastmonthproducts():
    cursor.execute('SELECT sum(quantity), product_name FROM cart, orderitem WHERE cart.id = orderitem.cart_id and is_paid = 1 and date between date_sub(now(), INTERVAL 1 MONTH) and now() group by product_name order by sum(quantity) desc')
    products = cursor.fetchall()
    return jsonify({'products': products})

@app.route('/most-product-last-week', methods=['GET'])
def lastweekproducts():
    cursor.execute('SELECT sum(quantity), product_name FROM cart, orderitem WHERE cart.id = orderitem.cart_id and is_paid = 1 and date between date_sub(now(), INTERVAL 1 WEEK) and now() group by product_name order by sum(quantity) desc')
    products = cursor.fetchall()
    return jsonify({'products': products})

app.run(debug=True)