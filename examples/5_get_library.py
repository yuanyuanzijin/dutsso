import sys
sys.path.append('.')
##################### 以上两行只是为了方便开发，实际不需要 #######################

import dutsso
import getpass
from prettytable import PrettyTable

u = dutsso.User(input('\n请输入学号：'), getpass.getpass('请输入密码：'))

login = u.login()
if login:
    # 获取借书信息
    lib_dict = u.get_library()
    print("\n————您的图书馆信息如下————")
    print("总借书次数：%s" % lib_dict['borrow_times'])
    print("违章次数：%s" % lib_dict['break_times'])
    print("欠费金额：%.2f" % float(lib_dict['break_money']))
    print("当前超期：%s" % lib_dict['overdue_nums'])
    print("预约到书：%s" % lib_dict['available_nums'])
    print("绑定邮箱：%s" % lib_dict['email'])
    print("绑定手机：%s" % lib_dict['phone'])

    print("\n————以下是当前详细借阅信息————")
    x = PrettyTable(["书名", "馆藏地", "借阅日期", "应还日期", "续借次数"])
    for i in lib_dict['current_borrow']:
        x.add_row([i['name'], i['location'], i['borrow_date'], i['before_date'], i['renew_times']])
    print(x)

else:
    print("用户名密码错误！")
