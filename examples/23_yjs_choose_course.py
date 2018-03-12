import dutsso
import getpass
from prettytable import PrettyTable

u = dutsso.User(input('\n请输入学号：'), getpass.getpass('请输入密码：'))

login = u.login()
if login:
    # 研究生选课
    course_list = u.get_course_not_choosed_yjs(other_classes=False)
    print("————未选择课程%d门————" % len(course_list))
    for i in course_list:
        if not i['c_full']: 
            print("\n——检测到未选择课程：%s，课程状态：可选" % i['c_name'])
            ch = input("是否选课？[y/n]")
            if (ch == "y" or ch == "Y"):
                back = u.choose_course_yjs(i, method="choose")
                if back:
                    print("%s选课成功！" % i['c_name'])
                else:
                    print("%s选课失败！" % i['c_name'])
            else:
                print("已取消操作")
                continue
        else:
            print("\n——检测到未选择课程%s，课程状态：已满" +i['c_name'])
            continue
else:
    print("用户名密码错误！")
    