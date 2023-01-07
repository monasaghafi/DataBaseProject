import mysql.connector
import datetime


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


try:
    mydb = mysql.connector.connect(host='localhost', user='root', password='5356600mre', database='mydb')
    if mydb.is_connected():
        cursor = mydb.cursor()
        cursor.execute('select id, date from cart where date < "' + str(datetime.date.today()) + '" and date > "' + last_month() + '"')
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

