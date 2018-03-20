import sys
sys.path.append('.')
##################### 以上两行只是为了方便开发，实际不需要 #######################

import dutsso
import getpass

u = dutsso.User(input('\n请输入学号：'), getpass.getpass('请输入密码：'))

login = u.login()
if login:
    # 获取校园邮箱信息
    email = u.get_email()
    print('————您的校园邮箱信息如下————')
    print("主邮箱：%s" % email['email'])
    print("未读邮件：%s" % email['unread'])
else:
    print("用户名密码错误！")
