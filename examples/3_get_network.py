import sys
sys.path.append('.')
##################### 以上两行只是为了方便开发，实际不需要 #######################

import dutsso
import getpass

u = dutsso.User(input('\n请输入学号：'), getpass.getpass('请输入密码：'))

login = u.login()
if login:
    # 获取校园网信息
    network = u.get_network()
    print('————您的校园网信息如下————')
    print("余额：%s元" % network['fee'])
    print("本月使用流量：%sMB" % network['used'])
else:
    print("用户名密码错误！")
    