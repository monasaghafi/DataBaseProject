import mysql.connector

try:
    mydb = mysql.connector.connect(host='localhost', user='root', password='alidev12345', database='mydb')
    if mydb.is_connected():
        cursor = mydb.cursor()
        cursor.execute('select * from user')
        records = cursor.fetchall()
        for r in records:
            print(r)
except:
    print('Error while connecting to MySQL!')


while True:
    print('please choose one option')
    print('1: sign up\n2: login\n3: exit')
    com = int(input())
    if com == 1:
        try:
            user = input('please enter your username:')
            password = input('please enter your password:')
            address = input('please enter your address:')
            phone = input('please enter your phone:')
            email = input('please enter your email:')
            bdate = input('please enter your brthdate:')
            sql = 'INSERT INTO user (password, name, address, phone, email, birthdate, role) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            val = (password, user, address, phone, email, bdate, 'user')
            cursor.execute(sql, val)
            mydb.commit()
        except:
            print('error')
    elif com == 2:
        pass
    elif com == 3:
        break

