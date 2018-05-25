import sys
sys.path.append('.')
##################### 以上两行只是为了方便开发，实际不需要 #######################

import getpass
import dutsso

username = input("请输入学号：")
password = getpass.getpass("请输入密码：")
u = dutsso.User(username=username, password=password)
login = u.login(try_cookies=False)
if not login:
    print("用户名或密码错误！")
    exit(-1)

print("明文方式登录成功！")

# 获取密文密码
encrypted_password = u.get_encrypted_password()
if encrypted_password:
    print("\n密文密码为：" + encrypted_password)
    print("再登录时可以使用该encrypted_password参数代替password参数，只要原密码不改变，该值是不变的。")
    print("在使用数据库储存账号密码时，请使用该值代替密码，尽管它也可以被解密还原，但至少比直接保存明文密码安全一些。")
else:
    print("登录失败！")

# 退出登录
u.logout()
print("\n已退出登录！下面进行密文登录演示：")

# 创建新对象进行密文密码登录演示
u2 = dutsso.User(username=username, encrypted_password=encrypted_password)

# 此处为了避免使用cookies直接跳过登录，才加入try_cookies参数，实际使用时建议优先使用cookies登录，即不填写此参数（因为默认为True）
login = u2.login(try_cookies=False)
if login:
    print("密文方式登录成功！")
else:
    print("密文方式登录失败，请确保获取密文密码时原密码输入正确！")