import dutsso
import getpass

u = dutsso.User(input('\n请输入学号：'), getpass.getpass('请输入密码：'))

login = u.login()
if login:
    # 获取浴室信息
    bath = u.get_bathroom()
    print("————浴室信息如下————")
    print("北山男浴室已使用%d/%d" % (bath['bs0']['use'], bath['bs0']['total']))
    print("北山女浴室已使用%d/%d" % (bath['bs1']['use'], bath['bs1']['total']))
    print("西山男浴室已使用%d/%d" % (bath['xs0']['use'], bath['xs0']['total']))
    print("西山女浴室已使用%d/%d" % (bath['xs1']['use'], bath['xs1']['total']))
else:
    print("用户名密码错误！")
