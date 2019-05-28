import sys
sys.path.append('.')
##################### 以上两行只是为了方便开发，实际不需要 #######################

import dutsso
import getpass
import requests

u = dutsso.User(input('\n请输入学号：'), getpass.getpass('请输入密码：'))

login = u.login()
if login:
    # 获取个人信息
    user_info = u.get_all_info()
    if user_info:
        print("————您的个人信息如下————")
        print("姓名：" + user_info['name'])
        print("性别：" + user_info['sex'])
        print("类别：" + user_info['type'])
        print("学部（院）：" + user_info['depart'])
        print("籍贯：" + user_info['home'])
        print("证件照：" + user_info['avatar'])
        print('\n* 证件照地址只有在登录状态下才可以查看，所以直接复制在浏览器里是不能查看的，除非浏览器处于登录状态。')
        print('* 这里提供save_avatar方法，可以直接下载至电脑中。')

        fname = 'avatar_%s.jpg' % u.username
        u.save_avatar(user_info['avatar'], save_path=fname)
        print('证件照下载完成！')

    else:
        print("信息获取失败！")
else:
    print("用户名密码错误！")
    