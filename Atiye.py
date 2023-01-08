import mysql.connector
from flask import Flask, jsonify, request, session

try:
    mydb = mysql.connector.connect(host='localhost', user='root', password='Boat9337', database='mydb')
    cursor = mydb.cursor(dictionary=True)
except:
    print('Error while connecting to MySQL!')

app = Flask(__name__)
app.secret_key = '4lid3v5ecr3t'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/users')
def getUsers():
    if not session['logged']:
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

@app.route('/orderlist', methods=['GET'])
def orderlist():
    if 'logged' in session.keys() and session['logged'] and session['role'] == 'superuser':
        cursor.execute('select * from cart,orderitem Where cart.id=orderitem.cart_id ')
        orders = cursor.fetchall()
        return jsonify({'orderlist': orders})
    elif 'logged' in session.keys() and session['logged'] and session['role'] == 'user':
        user_id = request.args.get('userid')
        cursor.execute('select * from cart,orderitem Where '
        +'cart.id=orderitem.cart_id and cart.customer_user_id = %s', (user_id,))
        orders = cursor.fetchall()
        return jsonify({'orderlist': orders})
    else:
        return jsonify({'message': 'You have to login first'})

@app.route('/supplierlist', methods=['GET'])
def supplierlist():
    if 'logged' in session.keys() and session['logged'] and session['role'] == 'superuser':
        productname = request.args.get('productname')
        cursor.execute ('select supplier.name, supplier.phone, supplier.address from ' + 
        'supplier,supplierproduct where supplier.id = supplierproduct.Supplier_id and ' + 
        'supplierproduct.Product_name = %s', (productname,))
        productname = cursor.fetchall()
        return jsonify({'productname': productname})
    else:
        return jsonify({'message': 'You have to login first'})

@app.route('/tenlastorder', methods=['GET'])
def tenlastorder():
    if 'logged' in session.keys() and session['logged']:
        user_id = request.args.get('userid')
        cursor.execute ('select * from cart,orderitem Where cart.id=orderitem.cart_id and ' + 
        'cart.customer_user_id = %s order by date DESC limit 10', (user_id,))
        orders = cursor.fetchall()
        return jsonify({'tenlastorder': orders})
    else:
        return jsonify({'message': 'You have to login first'})

@app.route('/productcomments', methods=['GET'])
def productcomments():
    pname = request.args.get('pname')
    cursor.execute('SELECT * FROM comment where product_name = %s', (pname,))
    comments = cursor.fetchall()
    return jsonify({'comments': comments})
    
app.run(debug=True)