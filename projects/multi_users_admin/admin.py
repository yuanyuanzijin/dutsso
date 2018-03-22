import sys
sys.path.append('.')
##################### 以上两行只是为了方便开发，实际不需要 #######################

import getpass
import sqlite3
import sys
import os
from prettytable import PrettyTable
import dutsso

user_list = {}

def title():
    os.system('clear')
    print("==================== 欢迎使用多用户管理系统 ====================")
    print("============ 本系统可以帮您更好地使用dutsso提供服务 ============")
    print("================ 本系统使用加密方式储存账号密码 ================")

def show_main():
    title()
    print("\n> 主菜单\n\n1.添加用户\n2.删除用户\n0.退出\n")

def show_one():
    title()
    print("\n> 主菜单 > 添加用户")

def show_two():
    title()
    print("\n> 主菜单 > 删除用户")
    user_list.clear()

    result = cursor.execute("SELECT username, success FROM Users").fetchall()
    if result:
        x = PrettyTable(["序号", "学号", "上次登录是否成功"])
        for index, i in enumerate(result):
            x.add_row([index+1, i[0], "是" if i[1] == "true" else "否"])
            user_list[str(index+1)] = i[0]
            print(x)
    else:
        print("无用户信息！")
    
db_path = os.path.join(sys.path[0], "users.db")
conn = sqlite3.connect(db_path)

cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS Users (id integer primary key autoincrement, username varchar, encrypted_password varchar, password_length int, success boolen)') 
conn.commit()

while 1:
    show_main()
    choice = input(">>> ")

    if choice == "1":
        while 1:
            show_one()
            username = input("\n请输入学号：")
            password = getpass.getpass("请输入密码：")
            c = input("确认添加用户%s？[Y/n]" % username)
            if not c or c in ['Y', 'y']:
                result = cursor.execute("SELECT * FROM Users where username='%s'" % username).fetchall()
                if not result:
                    u = dutsso.User(username=username, password=password)
                    login = u.login(show_info=False)
                    if login:
                        encrypted_password = u.get_encrypted_password()
                        cursor.execute("INSERT INTO Users (username, encrypted_password, password_length, success) VALUES ('%s', '%s', '%s', 'true')" % (username, encrypted_password, len(password)))
                        conn.commit()
                        print("用户%s创建成功！" % username)
                    else:
                        print("用户名密码错误，请重试！")
                else:
                    print("用户%s已存在，无需重复添加！" % username)

            print("\n按0返回主菜单，其他键继续添加")
            c2 = input(">>> ")
            if c2 == "0":
                break

    elif choice == "2":
        while 1:
            show_two()
            print("\n请选择序号进行删除，按0返回主菜单")
            c = input(">>> ")
            if c != "0":
                if c in user_list.keys():
                    username = user_list[c]
                    cursor.execute("DELETE FROM Users where username='%s'" % username)
                    conn.commit()
                    print("成功删除用户%s！" % username)
                else:
                    print("您的输入有误！")
                input("按任意键继续...")
            else:
                break

    elif choice == "0":
        print("感谢您的使用！")
        exit(0)

    else:
        print("您的输入不正确!")
        input("按任意键继续...")

