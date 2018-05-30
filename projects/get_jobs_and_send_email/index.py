import sys
sys.path.append('.')
##################### 以上两行只是为了方便开发，实际不需要 #######################

import os
import time
import sys
import dutsso

now = time.localtime(time.time())
search_date = "%d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday)

# 查询招聘信息
u = dutsso.User()
jobs = u.get_job(search_date=search_date)      # 默认为当天的
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

subject = "%s招聘信息汇总" % search_date
content = init_content(search_date, jobs)
config_path = os.path.join('mail_config.ini')

m = dutsso.Mail(config_path)

mail_list_path = os.path.join(sys.path[0], "mail_list.txt")
with open(mail_list_path) as f:
    emails = ["<%s>" % l.strip() for l in f.readlines()]
m.send(emails, subject, content)
