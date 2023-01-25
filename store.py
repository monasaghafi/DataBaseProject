import datetime

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
            cursor.execute('select * from user')
            #get data and convert to json
            records = cursor.fetchall()
            return jsonify({'users': records})
        else:
            return jsonify({'message': 'Only admins can see users info!'})

@app.route('/register', methods=['GET'])
def register():
    try:
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
    except:
        return jsonify({'message': 'please enter information correctly!'})

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

@app.route('/orderlist', methods=['GET'])
def orderlist():
    if 'logged' in session.keys() and session['logged'] and session['role'] == 'superuser':
        cursor.execute('select * from cart,orderitem Where cart.id=orderitem.cart_id ')
        orders = cursor.fetchall()
        return jsonify({'orderlist': orders})
    elif 'logged' in session.keys() and session['logged'] and session['role'] == 'user':
        cursor.execute('select * from cart,orderitem Where '
        + 'cart.id=orderitem.cart_id and cart.customer_user_id = ' + str(session['userid']) + '')
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
    if 'logged' in session.keys() and session['logged'] and session['role'] == 'superuser':
        user_id = request.args.get('userid')
        cursor.execute ('select * from cart,orderitem Where cart.id=orderitem.cart_id and ' + 
        'cart.customer_user_id = %s order by date DESC limit 10', (user_id,))
        orders = cursor.fetchall()
        return jsonify({'tenlastorder': orders})
    elif 'logged' in session.keys() and session['logged'] and session['role'] == 'user':
        cursor.execute ('select * from cart,orderitem Where cart.id=orderitem.cart_id and ' + 
        'cart.customer_user_id = ' + str(session['userid']) + ' order by date DESC limit 10')
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

@app.route('/productsales', methods=['GET'])
def productsales():
    if 'logged' in session.keys() and session['logged'] and session['role'] == 'superuser':
        productname = request.args.get('productname')
        cursor.execute('SELECT Product_name, sum(total), sum(quantity) from orderitem,cart' +
        ' where Product_name = %s and is_paid = 1 and Cart_id = cart.id and date between date_sub(now(),' +
        ' INTERVAL 1 month) and now()', (productname,))
        productlist = cursor.fetchall()
        return jsonify({'productsales': productlist})
    else:
        return jsonify({'message': 'You have to login first'})
    
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


@app.route('/MinSale', methods=['GET'])
def index_min_sale():
    if 'logged' in session.keys() and session['logged'] and session['role'] == 'superuser':
        pname = request.args.get('pname')
        query = 'SELECT product.name, product.price, product.brand, '
        query += 'supplier.id, supplier.name, supplier.phone, Min(product.price) '
        query += 'FROM supplier, supplierproduct, product '
        query += 'WHERE Supplier_id = supplier.id AND Product_name = product.name AND product.name LIKE %s'
        cursor.execute(query, ("{}%".format(pname),))
        records = cursor.fetchall()
        return jsonify({'MinSale': records})
    else:
        return jsonify({'error': 'You Do NOT have the access this page.'})


@app.route('/Top3Comments', methods=['GET'])
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


@app.route('/SameCity', methods=['GET'])
def index_same_city():
    city = request.args.get('city')
    query = 'SELECT id, name, address, phone, email, birthdate '
    query += 'FROM user '
    query += 'WHERE address LIKE "%' + city + '%" '
    cursor.execute(query)
    records = cursor.fetchall()
    return jsonify({'Users In Same City': records})


@app.route('/UserEdit/Delete', methods=['GET'])
def index_edit_delete():
    try:
        if 'logged' in session.keys() and session['logged'] and session['role'] == 'superuser':
            id = request.args.get('id', default=None, type=str)
            password = request.args.get('password', default=None, type=str)
            name = request.args.get('name', default=None, type=str)
            address = request.args.get('address', default=None, type=str)
            phone = request.args.get('phone', default=None, type=str)
            email = request.args.get('email', default=None, type=str)
            birthdate = request.args.get('birthdate', default=None, type=str)
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
            query += 'role = "user"' if is_first else ' AND role = "user"'
            if not is_first:
                cursor.execute(query)
                mydb.commit()
                return jsonify({'Admin Delete': 'DONE.'})
            else:
                return jsonify({'Admin Delete': 'Please enter correct info!'})
        else:
            return jsonify({'Admin Delete': 'You Do NOT have the access this page.'})
    except:
        return jsonify({'message': 'Please enter correct info!'})


@app.route('/UserEdit/Update', methods=['GET'])
def index_edit_update():
    try:
        if 'logged' in session.keys() and session['logged'] and session['role'] == 'superuser':
            id = request.args.get('id', default=None, type=str)
            password = request.args.get('password', default=None, type=str)
            name = request.args.get('name', default=None, type=str)
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
            query += ' WHERE id = "' + str(id) + '" And role = "user" '
            if id:
                cursor.execute(query)
                mydb.commit()
                return jsonify({'Admin Update': 'DONE.'})
            else:
                return jsonify({'Admin Delete': 'Please enter correct info!'})
        else:
            return jsonify({'Admin Update': 'You Do NOT have the access this page.'})
    except:
        return jsonify({'message': 'Please enter correct info!'})


@app.route('/UserEdit/Add', methods=['GET'])
def index_edit_add():
    try:
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
    except:
        return jsonify({'message': 'Please enter correct info!'})
    
@app.route('/ProductEdit/Update', methods=['GET'])  # update
def editProduct_Update():
    try:
        # حالتی که یوزر لاگین نشده
        if 'logged' not in session.keys() or not session['logged']:
            return jsonify({'message': 'please login first!'})
        # حالتی که یوزر ادمین هست
        elif 'logged' in session.keys() or session['logged'] and session['role'] == 'superuser':
            name = request.args.get('name', default=None)
            barcode = request.args.get('barcode', default=None)
            price = request.args.get('price', default=None)
            discount = request.args.get('discount', default=None)
            category = request.args.get('category', default=None)
            brand = request.args.get('brand', default=None)
            query = 'UPDATE product SET '
            is_first = True
            if barcode is not None:
                query += ('barcode = "' + barcode +
                        '"') if is_first else (', barcode = "' + barcode + '"')
                is_first = False
            if price is not None:
                query += ('price = "' + price +
                        '"') if is_first else (', price = "' + price + '"')
                is_first = False
            if discount is not None:
                query += ('discount = "' + discount +
                        '"') if is_first else (', discount = "' + discount + '"')
                is_first = False
            if category is not None:
                query += ('category = "' + category +
                        '"') if is_first else (', category = "' + category + '"')
                is_first = False
            if brand is not None:
                query += ('brand = "' + brand +
                        '"') if is_first else (', brand = "' + brand + '"')
                is_first = False
            query += ' WHERE name = "' + name + '" '
            if name:
                cursor.execute(query)
                mydb.commit()
                return jsonify({'Admin Update': 'Updating product is DONE.'})
            else:
                return jsonify({'Admin Delete': 'Please enter correct info!'})
        else:  # حالتی که یوزر ادمین نمی باشد
            return jsonify({'Admin Update': 'You Do NOT have access to this page.'})
    except:
        return jsonify({'message': 'Please enter correct info!'})


@app.route('/ProductEdit/Add', methods=['GET'])  # add
def editProduct_Add():
    try:
        # حالتی که یوزر لاگین نشده
        if 'logged' not in session.keys() or not session['logged']:
            return jsonify({'message': 'please login first!'})
        # حالتی که یوزر ادمین هست
        elif 'logged' in session.keys() or session['logged'] and session['role'] == 'superuser':
            name = request.args.get('name', default=None)
            barcode = request.args.get('barcode', default=None)
            price = request.args.get('price', default=None)
            discount = request.args.get('discount', default=None)
            category = request.args.get('category', default=None)
            brand = request.args.get('brand', default=None)
            query = 'INSERT INTO product (name, barcode, price, discount, category, brand) values ('
            if name is not None:
                query += '"' + name + '"'
            if barcode is not None:
                query += ', "' + barcode + '"'
            if price is not None:
                query += ', "' + price + '"'
            if discount is not None:
                query += ', "' + discount + '"'
            if category is not None:
                query += ', "' + category + '"'
            if brand is not None:
                query += ', "' + brand + '")'
            cursor.execute(query)
            mydb.commit()
            return jsonify({'Admin Update': 'Updating product is DONE.'})
        else:  # حالتی که یوزر ادمین نمی باشد
            return jsonify({'Admin Update': 'You Do NOT have access to this page.'})
    except:
        return jsonify({'message': 'Please enter correct info!'})    
    


@app.route('/ProductEdit/Delete', methods=['GET'])
def editProduct_Delete():
    try:
        # حالتی که یوزر لاگین نشده
        if 'logged' not in session.keys() or not session['logged']:
            return jsonify({'message': 'please login first!'})
        # حالتی که یوزر ادمین هست
        elif 'logged' in session.keys() or session['logged'] and session['role'] == 'superuser':
            name = request.args.get('name', default=None)
            barcode = request.args.get('barcode', default=None)
            price = request.args.get('price', default=None)
            discount = request.args.get('discount', default=None)
            category = request.args.get('category', default=None)
            brand = request.args.get('brand', default=None)
            is_first = True
            query = 'DELETE FROM Product '
            query += 'WHERE '
            if name is not None:
                query += ('name = "' + name +
                        '"') if is_first else ('AND name = "' + name + '"')
                is_first = False
            if barcode is not None:
                query += ('barcode = "' + barcode +
                        '"') if is_first else (' AND barcode = "' + barcode + '"')
                is_first = False
            if price is not None:
                query += ('price = "' + price +
                        '"') if is_first else (' AND price = "' + price + '"')
                is_first = False
            if discount is not None:
                query += ('discount = "' + discount +
                        '"') if is_first else (' AND discount = "' + discount + '"')
                is_first = False
            if category is not None:
                query += ('category = "' + category +
                        '"') if is_first else (' AND category = "' + category + '"')
                is_first = False
            if brand is not None:
                query += ('brand = "' + brand +
                        '"') if is_first else (' AND brand = "' + brand + '"')
                is_first = False
            if not is_first:
                cursor.execute(query)
                mydb.commit()
                return jsonify({'Admin Delete': 'DONE.'})
            else:
                return jsonify({'message': 'Please enter correct info!'})
        else:
            return jsonify({'Admin Delete': 'You Do NOT have the access this page.'})
    except:
        return jsonify({'message': 'Please enter correct info!'})
    
@app.route('/categories', methods=['GET'])
def getCategory():
    cursor.execute('select distinct category from product')
    category = cursor.fetchall()
    return jsonify({'category': category})


@app.route('/discount15%', methods=['GET'])
def get15discount():
    cursor.execute('select * from product where discount > 15')
    discount = cursor.fetchall()
    return jsonify({'discount': discount})

@app.route('/avgSoldMonth', methods=['GET'])
def avg_month():
    cursor.execute(
        'select avg(total_price) from cart where is_paid=1 and date between date_sub(now(), INTERVAL 1 MONTH) and now()')
    avgsold_month = cursor.fetchall()
    return jsonify({'avgsold_month': avgsold_month})

app.run(debug=True)