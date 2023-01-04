import mysql.connector

CurrentID = 0
CurrentRole = ''
try:
    mydb = mysql.connector.connect(host='localhost', user='root', password='5356600mre', database='mydb')
    if mydb.is_connected():
        cursor = mydb.cursor()
        cursor.execute("select * from user")
        records = cursor.fetchall()
        for r in records:
            for field in r:
                print(field, end="\t")
            print()
except:
    print('Error while connecting to MySQL!')

while True:
    print('please choose one option')
    print('1: sign up\n2: login\n3: exit')
    com = int(input())
    if com == 1:
        try:
            first = True
            while first or cursor.fetchone()[0] == 1:
                if not first:
                    print('this username is already taken')
                user = input('please enter your username:')
                sql = 'select count(*) from user where user.name = %s'
                cursor.execute(sql, [user])
                first = False
            password = input('please enter your password:')
            address = input('please enter your address:')
            phone = input('please enter your phone:')
            email = input('please enter your email:')
            bdate = input('please enter your brthdate:')
            sql = 'INSERT INTO user (password, name, address, phone, email, birthdate, role)\
             VALUES (%s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, [password, user, address, phone, email, bdate, 'user'])
            mydb.commit()
        except:
            print('error')
    elif com == 2:
        try:
            user = input('please enter your username:')
            password = input('please enter your password:')
            sql = 'select count(*) from user where user.password = %s and user.name = %s'
            val = (password, user)
            cursor.execute(sql, val)
            if cursor.fetchone()[0] == 1:
                print('You have enterd the system')
                sql = 'select id, role from user where user.password = %s and user.name = %s'
                val = (password, user)
                cursor.execute(sql, val)
                CurrentUser = cursor.fetchone()
                print(CurrentUser)
                CurrentID = CurrentUser[0]
                CurrentRole = CurrentUser[1]
                print('ID = ' + str(CurrentID))
                print('Role = ' + CurrentRole)
            else:
                print('No such user available')
        except:
            print('error')
    elif com == 3:
        break
