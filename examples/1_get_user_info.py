import sys
sys.path.append('.')
##################### 以上两行只是为了方便开发，实际不需要 #######################

import dutsso
import getpass

u = dutsso.User(input('\n请输入学号：'), getpass.getpass('请输入密码：'))

login = u.login()
if login:
    # 获取个人信息
    user_info = u.get_all_info()
    print("————您的个人信息如下————")
    print("姓名：" + user_info['name'])
    print("性别：" + user_info['sex'])
    print("类别：" + user_info['type'])
    print("学部（院）：" + user_info['depart'])
    print("籍贯：" + user_info['home'])
    print("证件照：" + user_info['avatar'])
else:
    print("用户名密码错误！")