import sys
sys.path.append('.')
##################### 以上两行只是为了方便开发，实际不需要 #######################

import dutsso
import getpass
from prettytable import PrettyTable

u = dutsso.User(input('\n请输入学号：'), getpass.getpass('请输入密码：'))

login = u.login()
if login:
    # 查询本科生成绩
    # course_type参数：all代表查看所有，bx代表知产看必修，xx代表只查看选修，rx代表只查看任选（不填默认为all）。
    # recently参数：True代表只查看本学期（近期）成绩，False代表查看本科阶段所有成绩（不填默认为False）。
    scores = u.get_score_bks(course_type="all", recently=True)
    print("\n————您的本学期成绩信息如下————")
    x = PrettyTable(["课程名称", "分数", "学分", "课程类型"])
    for i in scores:
        x.add_row([i['c_name'], i['c_value'], i['c_score'], i['c_type']])
    print(x)
