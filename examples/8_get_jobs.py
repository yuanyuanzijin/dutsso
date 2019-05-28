import sys
sys.path.append('.')
##################### 以上两行只是为了方便开发，实际不需要 #######################

import dutsso
from prettytable import PrettyTable

# 查询招聘信息
date = "2019-05-29"
u = dutsso.User()
jobs = u.get_job(search_date=date)      # 如不填默认获取当天的

print("\n———— %s招聘信息获取如下 ————" % date)
x = PrettyTable(["日期", "时间", "招聘会名称", "地址", "详细链接"])
for job in jobs:
    x.add_row([job['date'], job['time'], job['title'], job['location'], job['url']])
print(x)
