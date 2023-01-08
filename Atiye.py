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
        pass
    elif com == 2:
        pass
    elif com == 3:
        break