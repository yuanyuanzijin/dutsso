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
    print("================== 研究生新成绩提醒系统用户管理 ==================")
    print("============ 使用本系统前请确保已使用admin.py添加用户 ============")
    print("========================== 祝您使用愉快 ==========================\n")

def show_main():
    title()
    print("————Users表中的全部研究生用户如下————")
    result = cursor.execute("SELECT username, name, email, success FROM Users WHERE user_type='研究生'").fetchall()
    if result:
        x = PrettyTable(["序号", "学号", "姓名", "邮箱", "上次登录是否成功", "是否添加提醒"])
        for index, i in enumerate(result):
            r = cursor.execute("SELECT * FROM Score_yjs_users WHERE username='%s'" % i[0]).fetchall()
            x.add_row([index+1, i[0], i[1], i[2], "是" if i[3] == "true" else "否" ,"是" if r else "否"])
            user_list[str(index+1)] = i[0]
        print(x)
    else:
        print("无用户信息！本程序和admin.py共享数据库，如已添加用户，请检查数据库路径是否正确！")

    print("\n> 主菜单")
    print("\n1.全部设置提醒\n2.全部删除提醒\n3.指定序号设置提醒\n4.指定序号删除提醒\n0.退出\n")

def show_one():
    title()
    print("————Users表中的未设置提醒的研究生用户如下————")
    result = cursor.execute("SELECT username, name, user_type, success FROM Users WHERE user_type='研究生'").fetchall()
    if result:
        x = PrettyTable(["序号", "学号", "姓名", "是否添加提醒"])
        for index, i in enumerate(result):
            r = cursor.execute("SELECT * FROM Score_yjs_users WHERE username='%s'" % i[0]).fetchall()
            if r:
                continue
            x.add_row([index+1, i[0], i[1], "是" if r else "否"])
            user_list[str(index+1)] = i[0]
        print(x)
    else:
        print("无用户信息！本程序和admin.py共享数据库，如已添加用户，请检查数据库路径是否正确！")
    print("\n> 主菜单 > 设置提醒")

def show_two():
    title()
    print("————Users表中的已设置提醒的研究生用户如下————")
    result = cursor.execute("SELECT username, name, user_type, success FROM Users WHERE user_type='研究生'").fetchall()
    if result:
        x = PrettyTable(["序号", "学号", "姓名", "是否添加提醒"])
        for index, i in enumerate(result):
            r = cursor.execute("SELECT * FROM Score_yjs_users WHERE username='%s'" % i[0]).fetchall()
            if not r:
                continue
            x.add_row([index+1, i[0], i[1], "是" if r else "否"])
            user_list[str(index+1)] = i[0]
        print(x)
    else:
        print("无用户信息！本程序和admin.py共享数据库，如已添加用户，请检查数据库路径是否正确！")
    print("\n> 主菜单 > 删除提醒")

    
db_path = os.path.join("users.db")
conn = sqlite3.connect(db_path)

cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Score_yjs_users (
    id integer primary key autoincrement, 
    username varchar,
    score_nums int, 
    get_success boolen,
    send_success boolen,
    new_times int,
    update_time datetime,
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
)
''') 
conn.commit()

while 1:
    show_main()
    choice = input(">>> ")

    # 全部设置提醒
    if choice == "1":
        show_one()
        c = input("确认为以上全部用户设置新成绩提醒？[Y/n]")
        if not c or c in ['Y', 'y']:
            result = cursor.execute("SELECT username FROM Users").fetchall()
            nums = 0
            for username in result:
                r = cursor.execute("SELECT * FROM Score_yjs_users WHERE username='%s'" % username).fetchall()
                if not r:
                    cursor.execute("INSERT INTO Score_yjs_users (username, new_times) VALUES ('%s', '0')" % username)
                    conn.commit()
                    nums += 1
                    print("已为用户%s添加新成绩提醒！" % username)
            print("全部添加成功！共添加%d个用户！" % nums)
        input("\n按任意键返回主菜单...")

    elif choice == "2":
        show_two()
        c = input("确认删除以上全部用户的新成绩提醒？[Y/n]")
        if not c or c in ['Y', 'y']:
            result = cursor.execute("DELETE FROM Score_yjs_users")
            print("全部删除成功！")
        input("\n按任意键返回主菜单...")

    elif choice == "3":
        while 1:
            show_one()
            print("\n请选择序号进行设置，按0返回主菜单")
            c = input(">>> ")
            if c != "0":
                if c in user_list.keys():
                    username = user_list[c]
                    cursor.execute("INSERT INTO Score_yjs_users (username, new_times) VALUES ('%s', '0')" % username)
                    conn.commit()
                    print("成功为用户%s设置提醒！" % username)
                else:
                    print("您的输入有误！")
                input("按任意键继续...")
            else:
                break

    elif choice == "4":
        while 1:
            show_two()
            print("\n请选择序号进行设置，按0返回主菜单")
            c = input(">>> ")
            if c != "0":
                if c in user_list.keys():
                    username = user_list[c]
                    cursor.execute("DELETE FROM Score_yjs_users WHERE username='%s'" % username)
                    conn.commit()
                    print("成功删除用户%s的提醒！" % username)
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

