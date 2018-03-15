import os
import time
import dutsso

# 查询招聘信息
date = "2018-03-15"
u = dutsso.User()
jobs = u.get_job(search_date=date)
print("信息获取成功！")

# 发送邮件
def init_content(date, jobs_list):
    content = date + "招聘信息汇总"
    content += "<table>"
    content += "<thead><tr><td>时间</td><td>地点</td><td>公司</td></tr></thead><tbody>"
    for i in jobs_list:        
        content += "<tr><td>%s</td><td>%s</td><td><a href='%s'>%s</a></td></tr>" % (i['time'], i['location'], i['url'], i['title'])
    content += "</tbody></table>"
    return content

subject = "Get good jobs!"
content = init_content(date, jobs)
config_path = os.path.join('mail_config.ini')

m = dutsso.Mail()
m.init_from_file(config_path)
emails = ["<jinluyuan@vip.qq.com>"]
back = m.send(emails, subject, content)
if back:
    print("发送成功！")