import dutsso
import getpass
from prettytable import PrettyTable

u = dutsso.User(input('\n请输入学号：'), getpass.getpass('请输入密码：'))

login = u.login()
if login:
    # 研究生课程评价
    evaluate_list = u.get_evaluate_list_unfinished_yjs()
    print(evaluate_list)
    print("————共找到未评价课程%d门————" % len(evaluate_list))
    for i in evaluate_list:
        if not i['e_complete']:
            print("——————正在进行《%s》课程的评价——————" % i['e_name'])
            choice1 = input("请选择该课程的考试方式（取消请按P，不填默认为A）：\nA：闭卷考试\tB：开卷考试\tC：大作业方式\tD：其他方式\n")
            if not choice1:
                choice1 = "A"
            if choice1 not in ["A", "a", "B", "b", "C", "c", "D", "d"]:
                print("已取消")
                continue
            choice2 = input("请对本门课程进行总体评分（取消请按P，不填默认为A）：\nA\tB\tC\tD\n")
            if not choice2:
                choice2 = "A"
            if choice2 not in ["A", "a", "B", "b", "C", "c", "D", "d"]:
                print("已取消")
                continue
            remark = input("请输入您的评价（可为空）：\n")

            rank = input("请对老师进行排名（默认第1名）：\n")

            back = u.evaluate_course_yjs(i, choice_exam=choice1, choice_whole=choice2, remark_text=remark, rank=rank)
            if back:
                print(i['e_name'] + "评价成功！")
            else:
                print(i['e_name'] + "评价失败！")
else:
    print("用户名密码错误！")
    