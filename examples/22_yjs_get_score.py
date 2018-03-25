import sys
sys.path.append('.')
##################### 以上两行只是为了方便开发，实际不需要 #######################

import dutsso
import getpass
from prettytable import PrettyTable

u = dutsso.User(input('\n请输入学号：'), getpass.getpass('请输入密码：'))

login = u.login()
if login:
    # 查询研究生成绩
    scores = u.get_score_yjs()
    if scores != False:
        print("————您的研究生成绩信息如下————")
        x = PrettyTable(["课程名称", "分数", "学分", "课程类型"])
        for i in scores:
            x.add_row([i['c_name'], i['c_value'], i['c_score'], "必修" if i['compulsory'] else "选修"])
        print(x)
    else:
        print("用户认证发生错误！")
else:
    print("用户名密码错误！")
    