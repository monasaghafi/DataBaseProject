import datetime
import json
import mysql.connector
from flask import Flask, request

isAdmin = True

try:
    mydb = mysql.connector.connect(host='localhost', user='root', password='5356600mre', database='mydb')
except:
    print('Error while connecting to MySQL!')

app = Flask(__name__)


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
    cursor = mydb.cursor()
    cursor.execute('select name, price, discount, category, brand from product')
    records = cursor.fetchall()
    out = '<br>'
    for r in records:
        out += 'name: ' + r[0]
        out += ' - price: ' + str(r[1])
        out += ' - discount: ' + str(r[2])
        out += ' - category: ' + r[3]
        out += ' - brand: ' + r[4] + '<br>'
    return json.dumps(out)


@app.route('/Top10Shoppers/Month')
def index_top10shoppers_month():
    cursor = mydb.cursor()
    query = 'SELECT distinct user.id, user.name, user.address, user.phone, count(user.id) as number_of_purchases '
    query += 'FROM cart, user '
    query += 'WHERE cart.Customer_user_id = user.id and '
    query += 'date < "' + str(datetime.date.today()) + '" and date > "' + last_month() + '" '
    query += 'GROUP BY user.id '
    query += 'ORDER BY number_of_purchases DESC'
    cursor.execute(query)
    records = cursor.fetchall()
    out = '<br>'
    num = 0
    for r in records:
        if num != 10:
            out += 'id: ' + str(r[0])
            out += ' - name: ' + str(r[1])
            out += ' - address: ' + str(r[2])
            out += ' - phone: ' + str(r[3])
            out += ' - number_of_purchases: ' + str(r[4]) + '<br>'
            num += 1
    return json.dumps(out)


@app.route('/Top10Shoppers/Week')
def index_top10shoppers_week():
    cursor = mydb.cursor()
    query = 'SELECT distinct user.id, user.name, user.address, user.phone, count(user.id) as number_of_purchases '
    query += 'FROM cart, user '
    query += 'WHERE cart.Customer_user_id = user.id and '
    query += 'date < "' + str(datetime.date.today()) + '" and date > "' + last_week() + '" '
    query += 'GROUP BY user.id '
    query += 'ORDER BY number_of_purchases DESC'
    cursor.execute(query)
    records = cursor.fetchall()
    out = '<br>'
    num = 0
    for r in records:
        if num != 10:
            out += 'id: ' + str(r[0])
            out += ' - name: ' + str(r[1])
            out += ' - address: ' + str(r[2])
            out += ' - phone: ' + str(r[3])
            out += ' - number_of_purchases: ' + str(r[4]) + '<br>'
            num += 1
    return json.dumps(out)


@app.route('/MinSale')
def index_min_sale():
    if isAdmin:
        cursor = mydb.cursor()
        query = 'SELECT product.name, product.price, product.brand, '
        query += 'supplier.id, supplier.name, supplier.phone, Min(product.price) '
        query += 'FROM supplier, supplierproduct, product '
        query += 'WHERE Supplier_id = supplier.id AND Product_name = product.name '
        query += 'GROUP BY product.name '
        cursor.execute(query)
        records = cursor.fetchall()
        out = '<br>'
        for r in records:
            out += 'name: ' + str(r[0])
            out += ' - price: ' + str(r[1])
            out += ' - brand: ' + str(r[2])
            out += ' - supplier.id: ' + str(r[3])
            out += ' - supplier.name: ' + str(r[4])
            out += ' - supplier.phone: ' + str(r[5]) + '<br>'
    else:
        out = 'You Do NOT have the access this page.'
    return json.dumps(out)


@app.route('/Top3Comments/', methods=['GET'])
def index_top3comments():
    pname = request.args.get('pname')
    cursor = mydb.cursor()
    query = 'SELECT name, Product_name, text, date, rate '
    query += 'FROM comment, user '
    query += 'WHERE Product_name = "' + pname + '" AND user.id = Customer_user_id '
    query += 'ORDER BY rate DESC '
    cursor.execute(query)
    records = cursor.fetchall()
    out = '<br>'
    num = 0
    for r in records:
        if num != 3:
            out += 'name: ' + str(r[0])
            out += ' - product name: ' + str(r[1])
            out += ' - text: ' + str(r[2])
            out += ' - date: ' + str(r[3])
            out += ' - rate: ' + str(r[4]) + '<br>'
            num += 1
    return json.dumps(out)


@app.route('/SameCity/', methods=['GET'])
def index_same_city():
    city = request.args.get('city')
    cursor = mydb.cursor()
    query = 'SELECT id, name, address, phone, email, birthdate '
    query += 'FROM user '
    query += 'WHERE address LIKE "%' + city + '%" '
    cursor.execute(query)
    records = cursor.fetchall()
    out = '<br>'
    for r in records:
        out += 'name: ' + str(r[0])
        out += ' - product name: ' + str(r[1])
        out += ' - text: ' + str(r[2])
        out += ' - date: ' + str(r[3])
        out += ' - rate: ' + str(r[4]) + '<br>'
    return json.dumps(out)


app.run()
