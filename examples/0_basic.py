import sys
sys.path.append('.')
##################### 以上两行只是为了方便开发，实际不需要 #######################

import getpass
import dutsso

# 创建User对象(方法一)
username = input('\n请输入学号：')
password = getpass.getpass('请输入密码：')
u = dutsso.User(username, password)

# 创建User对象（方法二）
# u = dutsso.User()
# u.username = input('\n请输入学号：')
# u.password = getpass.getpass('请输入密码：')

# 登录
login = u.login()
if login:
    print("%s（%s）登录成功！" % (u.name, u.type))
else:
    print("用户名密码错误！")

# 检测登录状态
if u.isactive():
    print("当前处于登录状态")
else:
    print("登录状态失效")

# 退出登录
u.logout()