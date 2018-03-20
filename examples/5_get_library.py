import sys
sys.path.append('.')
##################### 以上两行只是为了方便开发，实际不需要 #######################

import dutsso
import getpass

u = dutsso.User(input('\n请输入学号：'), getpass.getpass('请输入密码：'))

login = u.login()
if login:
    # 获取借书信息
    lib_dict = u.get_library()
    print("————您的图书馆信息如下————")
    print("总借书次数：%s" % lib_dict['times'])
    print("欠费金额：%s" % lib_dict['money'])
    print("绑定邮箱：%s" % lib_dict['email'])
    print("绑定手机：%s" % lib_dict['phone'])
else:
    print("用户名密码错误！")
