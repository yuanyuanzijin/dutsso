import sys
sys.path.append('.')
##################### 以上两行只是为了方便开发，实际不需要 #######################

import dutsso
import getpass

u = dutsso.User(input('\n请输入学号：'), getpass.getpass('请输入密码：'))

login = u.login()
if login:
    # 获取玉兰卡信息
    card = u.get_card()
    print("————您的校园卡信息如下————")
    print("余额：%s元" % card["money"])
    print("最后交易时间：%s" % card["last_time"])
else:
    print("用户名密码错误！")
    