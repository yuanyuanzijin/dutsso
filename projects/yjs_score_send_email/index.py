import sys
sys.path.append('.')
##################### 以上两行只是为了方便开发，实际不需要 #######################

import sqlite3
import sys
import os
import time
import dutsso

def send_email(scores, obj):
    if obj.first_use:
        subject = "欢迎使用新成绩提醒系统(新版）！"
        content = "<p>%s您好，您已订阅新成绩提醒系统，我们将在检测新成绩后为您推送邮件~</p>" % obj.name
    else:
        subject = "发现新成绩！"
        content = "<p>%s您好，发现一条新成绩</p>" % obj.name
        
    content += '<p>共找到%d条成绩</p><hr />' % len(scores)
    content += "<div><table>"
    content += "<thead><tr><td>课程名称</td><td>课程类型</td><td>学分</td><td>分数</td></tr></thead><tbody>"
    for i in scores:
        c_type = "必修" if i['compulsory'] else "选修"
        content += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (i['c_name'], c_type, i['c_score'], i['c_value'])
    content += "</tbody></table></div>"

    content += "<hr /><p>我的Github主页：<a href='https://github.com/yuanyuanzijin'>https://github.com/yuanyuanzijin</a></p><p>Powered by Zijin</p>"
    back = m.send(obj.emailaddr, subject, content)
    return back

def dict_factory(cursor, row):  
    d = {}  
    for idx, col in enumerate(cursor.description):  
        d[col[0]] = row[idx]  
    return d  

config_path = os.path.join('mail_config.ini')
m = dutsso.Mail()
m.init_from_file(config_path)

db_path = os.path.join("users.db")
conn = sqlite3.connect(db_path)
conn.row_factory = dict_factory  
cursor = conn.cursor()

users = cursor.execute("SELECT a.*, b.* FROM Score_yjs_users a, Users b WHERE a.username=b.username").fetchall()
print("检测到%d个提醒用户" % len(users))

for i in range(len(users)):
    u = dutsso.User()
    u.username = users[i]['username']
    u.encrypted_password = users[i]['encrypted_password']

    u.emailaddr = users[i]['email']
    u.first_use = True if users[i]['score_nums'] == None else False
    old_nums = users[i]['score_nums']
    if old_nums == None:
        old_nums = 0

    login = u.login()
    if login:
        print(u.name + "登录成功！")
        scores = u.get_score_yjs()
        if scores != False:
            cursor.execute("UPDATE Score_yjs_users SET get_success='true' WHERE username='%s'" % u.username)
            print(len(scores))
            if len(scores) > old_nums:
                back = send_email(scores, u)
                if back:
                    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
                    cursor.execute("UPDATE Score_yjs_users SET score_nums='%d', new_times=new_times+1, send_success='true', update_time='%s' WHERE username='%s'" 
                        % (len(scores), now, u.username))
                    print("邮件发送成功！")
                else:
                    cursor.execute("UPDATE Score_yjs_users SET send_success='false' WHERE username='%s'" % u.username)                
                    print("邮件发送失败")
                conn.commit()
            else:
                print("未发现新成绩！")
        else:
            cursor.execute("UPDATE Score_yjs_users SET get_success='false' WHERE username='%s'" % u.username)
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET success='false' WHERE username='%s'" % u.username)
        print("用户名密码错误！")

            