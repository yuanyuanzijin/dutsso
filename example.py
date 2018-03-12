import getpass
import dutsso
from bs4 import BeautifulSoup
from prettytable import PrettyTable

print('\n********** 欢迎使用大连理工大学校园门户信息查询系统 **********')
print('******************** Powered by Zijin ********************')

u = dutsso.User(input('\n请输入学号：'), getpass.getpass('请输入密码：'))
# SSO登录
login = u.login()

if not login:
    print("用户名密码错误！")
else:
    print("%s（%s）登录成功！" % (u.name, u.type))

    # 获取个人信息
    user_info = u.get_all_info()
    print("\n*****您的个人信息如下：")
    print("姓名：" + user_info['name'])
    print("性别：" + user_info['sex'])
    print("类别：" + user_info['type'])
    print("学部（院）：" + user_info['depart'])
    print("籍贯：" + user_info['home'])
    print("手机：" + user_info['mobile'])
    print("邮箱：" + user_info['email'])

    # 查询校园卡余额
    if u.isactive():
        card = u.get_card()
        print("\n*****您的校园卡信息为：")
        print("余额：%s元" % card["money"])
        print("最后交易时间：%s" % card["last_time"])

    # 获取校园网信息
    if u.isactive():
        network = u.get_network()
        print('\n*****您的校园网信息为：')
        print("余额：%s元" % network['fee'])
        print("本月使用流量：%sMB" % network['used'])

    # 获取校园邮箱信息
    if u.isactive():
        email = u.get_email()
        print('\n*****您的校园邮箱信息为：')
        print("主邮箱：%s" % email['email'])
        print("未读邮件：%s" % email['unread'])

    # 查询浴室信息
    if u.isactive():
        bath = u.get_bathroom()
        print("\n*****浴室信息如下：")
        print("北山男浴室已使用%d/%d" % (bath['bs0']['use'], bath['bs0']['total']))
        print("北山女浴室已使用%d/%d" % (bath['bs1']['use'], bath['bs1']['total']))
        print("西山男浴室已使用%d/%d" % (bath['xs0']['use'], bath['xs0']['total']))
        print("西山女浴室已使用%d/%d" % (bath['xs1']['use'], bath['xs1']['total']))

    # 查询研究生成绩
    if u.isactive():
        scores = u.get_score_yjs()
        print("\n*****您的研究生成绩信息为：")
        x = PrettyTable(["课程名称", "分数", "学分", "课程类型"])
        for i in scores:
            x.add_row([i['c_name'], i['c_value'], i['c_score'], "必修" if i['compulsory'] else "选修"])
        print(x)

    # 查询研究生培养方案
    if u.isactive():
        plan_dict = u.get_plan_yjs()
        plans = plan_dict['plan']
        print("\n*****您的研究生培养方案为：")
        print(plan_dict['teacher'])
        print(plan_dict['required'])
        print(plan_dict['general'])
        x = PrettyTable(["课程名称", "课程类别", "是否必修课", "学分", "学时", "开课学期"])
        for i in plans:
            x.add_row([i['p_name'], i['p_type'], "必修" if i['p_compulsory'] else "选修", i['p_score'], i['p_time'], i['p_term']])
        print(x)

    # 查询图书馆
    if u.isactive():
        lib_dict = u.get_library()
        print("\n*****您的图书馆信息为：")
        print("总借书次数：%s" % lib_dict['times'])
        print("欠费金额：%s" % lib_dict['money'])
        print("绑定邮箱：%s" % lib_dict['email'])
        print("绑定手机：%s" % lib_dict['phone'])

    # 研究生选课系统
    if u.isactive():
        course_list = u.get_course_not_choosed_yjs(other_classes=False)
        print("\n*****检测到未选择课程%d门" % len(course_list))
        for i in course_list:
            if not i['c_full']: 
                print("\n***检测到未选择课程：%s，课程状态：可选" % i['c_name'])
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
                print("***检测到未选择课程%s，课程状态：已满" +i['c_name'])
                continue

    # 研究生课程评价
    if u.isactive():
        evaluate_list = u.get_evaluate_list_unfinished_yjs()
        for i in evaluate_list:
            if i['e_complete']:
                print("\n——————正在进行《%s》课程的评价——————" % i['e_name'])
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
            
    u.logout()

input('\n按Enter键退出...')