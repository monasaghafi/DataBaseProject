import datetime
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

def last_month():
    today = datetime.date.today()
    out = ""
    if int(today.month) == 1:
        out += str(int(today.year) - 1) + '-'
        out += '12-'
        out += str(today.day) if int(today.day) > 9 else ('0' + str(today.day))
    else:
        out += str(today.year) + '-'
        out += str(int(today.month) - 1) if int(today.month) > 10 else ('0' + str(int(today.month) - 1)) + '-'
        out += str(today.day) if int(today.day) > 9 else ('0' + str(today.day))
    return out




################### selections ###################

 # select distinct category from product
@app.route('/categories', methods=['GET'])
def getCategory():
    cursor.execute('select distinct category from product')
    category = cursor.fetchall()
    return jsonify({'category': category})



 #select * from product where discount > 14;
@app.route('/discount15%', methods=['GET'])
def get15discount():
    cursor.execute('select * from product where discount > 14')
    category = cursor.fetchall()
    return jsonify({'category': category})




################### User ###################
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



@app.route('/ProductEdit/Update', methods=['GET']) #update
def editProduct_Update():
    if 'logged' not in session.keys() or not session['logged']: #حالتی که یوزر لاگین نشده
        return jsonify ({'message':'please login first!'})
    elif 'logged' in session.keys() or session['logged'] and session['role'] == 'superuser': #حالتی که یوزر ادمین هست
        name = request.args.get('name', default=None)
        barcode = request.args.get('barcode', default=None)
        price = request.args.get('price', default=None)
        discount = request.args.get('discount', default=None)
        category = request.args.get('category', default=None)
        brand = request.args.get('brand', default=None)
        query = 'UPDATE product SET '
        is_first = True
        if name is not None:
            query += ('name = "' + name + '"') if is_first else (', name = "' + name + '"')
            is_first = False
        if barcode is not None:
            query += ('barcode = "' + barcode + '"') if is_first else (', barcode = "' + barcode + '"')
            is_first = False
        if price is not None:
            query += ('price = "' + price + '"') if is_first else (', price = "' + price + '"')
            is_first = False
        if discount is not None:
            query += ('discount = "' + discount + '"') if is_first else (', discount = "' + discount + '"')
            is_first = False
        if category is not None:
            query += ('category = "' + category + '"') if is_first else (', category = "' + category + '"')
            is_first = False
        if brand is not None:
            query += ('brand = "' + brand + '"') if is_first else (', brand = "' + brand + '"')
            is_first = False
        query += ' WHERE id = "' + id + '"'
        cursor.execute(query)
        mydb.commit()
        return jsonify({'Admin Update': 'Updating product is DONE.'})
    else : #حالتی که یوزر ادمین نمی باشد
            return jsonify({'Admin Update': 'You Do NOT have the access this page.'})


@app.route('/ProductEdit/Add', methods=['GET']) #add
def editProduct_Add():
     if 'logged' in session.keys() and session['logged'] and session['role'] == 'superuser':
        password = request.args.get('password', default='12345', type=str)
        name = request.args.get('name', default=None, type=str)
        address = request.args.get('address', default=None, type=str)
        phone = request.args.get('phone', default=None, type=str)
        email = request.args.get('email', default=None, type=str)
        birthdate = request.args.get('birthdate', default=None, type=str)
        role = request.args.get('role', default=None, type=str)
        query = 'INSERT INTO user ( password, name'
        if address is not None:
            query += ', address'
        if phone is not None:
            query += ', phone'
        if email is not None:
            query += ', email'
        if birthdate is not None:
            query += ', birthdate'
        query += ', role ) VALUES ( '
        if password is not None:
            query += '"' + password + '"'
        if name is not None:
            query += ', "' + name + '"'
        if address is not None:
            query += ', "' + address + '"'
        if phone is not None:
            query += ', "' + phone + '"'
        if email is not None:
            query += ', "' + email + '"'
        if birthdate is not None:
            query += ', "' + birthdate + '"'
        query += ', "' + role + '" )'
        cursor.execute(query)
        mydb.commit()
        return jsonify({'Admin Add': 'DONE.'})
    else:
        return jsonify({'Admin Add': 'You Do NOT have the access this page.'})








# @app.route('/categories', methods=['GET'])
# def avgSoldMonth():


app.run(debug=True)