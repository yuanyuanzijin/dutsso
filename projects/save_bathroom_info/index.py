import sys
sys.path.append('.')
##################### 以上两行只是为了方便开发，实际不需要 #######################

import getpass
import sqlite3
import time
import sys
import os
import configparser
import dutsso

config_path = os.path.join(sys.path[0], "single_user_config.ini")

if not os.path.exists(config_path):
    print("请检查配置文件的路径！并请确保已将项目中的single_user_config.ini.example重命名为single_user_config.ini")

c = configparser.ConfigParser()
try:
    with open(config_path) as f:
        c.readfp(f)
        username = c.get('user', 'username')
        encrypted_password = c.get('user', 'encrypted_password')
        password_length = c.get('user', 'password_length')
except:
    print("single_user_config.ini配置文件格式有误，请检查重试！")
    exit(-1)

u = dutsso.User(username=username, encrypted_password=encrypted_password, password_length=password_length)
login = u.login(show_info=False)
if not login:
    print("登录失败！")
    exit(-1)

bath = u.get_bathroom()
data_bs0 = bath['bs0']['use']
data_bs1 = bath['bs1']['use']
data_xs0 = bath['xs0']['use']
data_xs1 = bath['xs1']['use']

db_path = os.path.join(sys.path[0], "bathroom.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
time = time.strftime('%H:%M', time.localtime(time.time()))
text = "insert into bathroom (`id`, `date`, `time`, `bs0`, `bs1`, `xs0`, `xs1`) values (null, '%s', '%s', '%d', '%d', '%d', '%d')" % (date, time, data_bs0, data_bs1, data_xs0, data_xs1)
cursor.execute(text)
print("%s %s 已成功写入数据库！" % (date, time))
cursor.close()
conn.commit()
conn.close()