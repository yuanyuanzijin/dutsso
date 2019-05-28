import sys
sys.path.append('.')
##################### 以上两行只是为了方便开发，实际不需要 #######################

import dutsso
import getpass
from prettytable import PrettyTable

u = dutsso.User(input('\n请输入学号：'), getpass.getpass('请输入密码：'))

login = u.login()
if login:
    # 获取所有可评价研究生课程
    evaluate_list = u.get_evaluate_list_yjs()
    print("\n————所有可评价研究生课程如下————")
    x = PrettyTable(["课程名称", "授课教师", "是否评价", "序号"])
    for index, e in enumerate(evaluate_list):
        x.add_row([e['e_name'], e['e_teacher'], "是" if e['e_complete'] else "否", index+1])
    print(x)

    # 课程评价（包括评价修改）
    while True:
        ch = input("\n请输入课程序号开始评价，如已评价则为评价修改（q退出）：")
        if ch in ['Q', 'q']:
            print('已退出')
            break
        try:
            ch = int(ch)
        except:
            print('序号输入有误！')
            continue

        if ch not in range(1, index+2):
            print('序号输入有误！')
            continue

        # 开始评价
        i = evaluate_list[ch-1]
        content = "修改" if i['e_complete'] else "新评价"
        print("\n——————正在进行《%s》课程的评价，状态：%s——————" % (i['e_name'], content))
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
    