import sys
sys.path.append('.')
##################### 以上两行只是为了方便开发，实际不需要 #######################

import os
import dutsso

# 创建Mail对象
m = dutsso.Mail()

# 初始化邮箱配置
config_path = os.path.join('mail_config.ini')
m.init_from_file(config_path)

# 发送邮件
subject = "欢迎使用dutsso"
content = "使用dutsso，分分钟成为编程大神，迎娶白富美！<hr />"
content += "<p>Github主页：<a href='https://github.com/yuanyuanzijin/dutsso'>https://github.com/yuanyuanzijin/dutsso</a></p><p>Powered by ZijinAI</p>"
emails = ["12345@qq.com"]
back = m.send(emails, subject, content)
if back:
    print("发送成功！")