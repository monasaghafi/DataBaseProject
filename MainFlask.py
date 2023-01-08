import datetime
import json
import mysql.connector
from flask import Flask, request, jsonify, session

isAdmin = True

try:
    mydb = mysql.connector.connect(host='localhost', user='root', password='5356600mre', database='mydb')
    cursor = mydb.cursor(dictionary=True)
except:
    print('Error while connecting to MySQL!')

app = Flask(__name__)
app.secret_key = '4lid3v5ecr3t'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


def last_week():
    today = datetime.date.today()
    out = ""
    if int(today.day) < 8:
        if int(today.month) == 1:
            out += str(int(today.year) - 1) + '-'
            out += '12-'
        else:
            out += str(today.year) + '-'
            out += str(int(today.month) - 1) if int(today.month) > 10 else ('0' + str(int(today.month) - 1)) + '-'
        out += str(((int(today.day) - 8) % 30) + 1)
    else:
        out = str(today.year) + '-'
        out += str(today.month) if int(today.month) > 9 else ('0' + str(today.month)) + '-'
        out += str(int(today.day) - 7) if int(today.day) > 16 else ('0' + str(int(today.day) - 7))
    return out


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


@app.route('/products')
def index_products():
    cursor.execute('select name, price, discount, category, brand from product')
    records = cursor.fetchall()
    return jsonify({'products': records})


@app.route('/Top10Shoppers/Month')
def index_top10shoppers_month():
    query = 'SELECT distinct user.id, user.name, user.address, user.phone, count(user.id) as number_of_purchases '
    query += 'FROM cart, user '
    query += 'WHERE cart.Customer_user_id = user.id and '
    query += 'date < "' + str(datetime.date.today()) + '" and date > "' + last_month() + '" '
    query += 'GROUP BY user.id '
    query += 'ORDER BY number_of_purchases DESC '
    query += 'LIMIT 10'
    cursor.execute(query)
    records = cursor.fetchall()
    return jsonify({'Top 10 Shoppers Of The Month': records})


@app.route('/Top10Shoppers/Week')
def index_top10shoppers_week():
    query = 'SELECT distinct user.id, user.name, user.address, user.phone, count(user.id) as number_of_purchases '
    query += 'FROM cart, user '
    query += 'WHERE cart.Customer_user_id = user.id and '
    query += 'date < "' + str(datetime.date.today()) + '" and date > "' + last_week() + '" '
    query += 'GROUP BY user.id '
    query += 'ORDER BY number_of_purchases DESC '
    query += 'LIMIT 10'
    cursor.execute(query)
    records = cursor.fetchall()
    return jsonify({'Top 10 Shoppers Of The Week': records})


@app.route('/MinSale/', methods=['GET'])
def index_min_sale():
    if isAdmin:
        pname = request.args.get('pname')
        query = 'SELECT product.name, product.price, product.brand, '
        query += 'supplier.id, supplier.name, supplier.phone, Min(product.price) '
        query += 'FROM supplier, supplierproduct, product '
        query += 'WHERE Supplier_id = supplier.id AND Product_name = product.name AND product.name LIKE "' + pname + '-%"'
        cursor.execute(query)
        records = cursor.fetchall()
        return jsonify({'MinSale': records})
    else:
        return jsonify({'error': 'You Do NOT have the access this page.'})


@app.route('/Top3Comments/', methods=['GET'])
def index_top3comments():
    pname = request.args.get('pname')
    query = 'SELECT name, Product_name, text, date, rate '
    query += 'FROM comment, user '
    query += 'WHERE Product_name = "' + pname + '" AND user.id = Customer_user_id '
    query += 'ORDER BY rate DESC '
    query += 'LIMIT 3'
    cursor.execute(query)
    records = cursor.fetchall()
    return jsonify({'Top 3 Comments': records})


@app.route('/SameCity/', methods=['GET'])
def index_same_city():
    city = request.args.get('city')
    query = 'SELECT id, name, address, phone, email, birthdate '
    query += 'FROM user '
    query += 'WHERE address LIKE "%' + city + '%" '
    cursor.execute(query)
    records = cursor.fetchall()
    return jsonify({'Users In Same City': records})


@app.route('/UserEdit/Delete/', methods=['GET'])
def index_edit_delete():
    if isAdmin:
        id = request.args.get('id', default=None, type=str)
        password = request.args.get('password', default=None, type=str)
        name = request.args.get('name', default=None, type=str)
        address = request.args.get('address', default=None, type=str)
        phone = request.args.get('phone', default=None, type=str)
        email = request.args.get('email', default=None, type=str)
        birthdate = request.args.get('birthdate', default=None, type=str)
        role = request.args.get('role', default=None, type=str)
        is_first = True
        query = 'DELETE FROM user '
        query += 'WHERE '
        if id is not None:
            query += 'id = "' + id + '"'
            is_first = False
        if password is not None:
            query += ('password = "' + password + '"') if is_first else (' AND password = "' + password + '"')
            is_first = False
        if name is not None:
            query += ('name = "' + name + '"') if is_first else (' AND name = "' + name + '"')
            is_first = False
        if address is not None:
            query += ('address = "' + address + '"') if is_first else (' AND address = "' + address + '"')
            is_first = False
        if phone is not None:
            query += ('phone = "' + phone + '"') if is_first else (' AND phone = "' + phone + '"')
            is_first = False
        if email is not None:
            query += ('email = "' + email + '"') if is_first else (' AND email = "' + email + '"')
            is_first = False
        if birthdate is not None:
            query += ('birthdate = "' + birthdate + '"') if is_first else (' AND birthdate = "' + birthdate + '"')
            is_first = False
        if role is not None:
            query += ('role = "' + role + '"') if is_first else (' AND role = "' + role + '"')
        cursor.execute(query)
        mydb.commit()
        return jsonify({'Admin Delete': 'DONE.'})
    else:
        return jsonify({'Admin Delete': 'You Do NOT have the access this page.'})


@app.route('/UserEdit/Update/', methods=['GET'])
def index_edit_update():
    if isAdmin:
        id = request.args.get('id', default=None, type=str)
        password = request.args.get('password', default=None, type=str)
        name = request.args.get('name', default=None, type=str)
        address = request.args.get('address', default=None, type=str)
        phone = request.args.get('phone', default=None, type=str)
        email = request.args.get('email', default=None, type=str)
        birthdate = request.args.get('birthdate', default=None, type=str)
        role = request.args.get('role', default=None, type=str)
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
        if role is not None:
            query += ('role = "' + role + '"') if is_first else (', role = "' + role + '"')
        query += ' WHERE id = "' + id + '"'
        cursor.execute(query)
        mydb.commit()
        return jsonify({'Admin Update': 'DONE.'})
    else:
        return jsonify({'Admin Update': 'You Do NOT have the access this page.'})


@app.route('/UserEdit/Add/', methods=['GET'])
def index_edit_add():
    if isAdmin:
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


app.run()
