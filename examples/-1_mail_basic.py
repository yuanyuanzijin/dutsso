import sys
sys.path.append('.')
##################### 以上两行只是为了方便开发，实际不需要 #######################

import os
import dutsso

# 创建Mail对象并初始化邮箱配置
m = dutsso.Mail(config_path='mail_config.ini')

# 发送邮件
subject = "欢迎使用dutsso"
content = '''
<p>使用dutsso，分分钟成为编程大神，迎娶白富美！</p><hr />
<p>Github主页：<a href='https://github.com/yuanyuanzijin/dutsso'>https://github.com/yuanyuanzijin/dutsso</a></p>
<p>Powered by ZijinAI</p>
'''
emailto = ["jinluyuan@vip.qq.com"]
attachment = ["README.rst", "setup.py"]         # V0.10.5版本加入添加附件功能，可为空

m.send(emailto, subject, content, attachment)
