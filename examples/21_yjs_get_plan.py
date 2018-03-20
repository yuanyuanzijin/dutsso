import sys
sys.path.append('.')
##################### 以上两行只是为了方便开发，实际不需要 #######################

import dutsso
import getpass
from prettytable import PrettyTable

u = dutsso.User(input('\n请输入学号：'), getpass.getpass('请输入密码：'))

login = u.login()
if login:
    # 查询研究生培养方案
    plan_dict = u.get_plan_yjs()
    plans = plan_dict['plan']
    print("————您的研究生培养计划如下————")
    print(plan_dict['teacher'])
    print(plan_dict['required'])
    print(plan_dict['general'])
    x = PrettyTable(["课程名称", "课程类别", "是否必修课", "学分", "学时", "开课学期"])
    for i in plans:
        x.add_row([i['p_name'], i['p_type'], "必修" if i['p_compulsory'] else "选修", i['p_score'], i['p_time'], i['p_term']])
    print(x)
else:
    print("用户名密码错误！")
    