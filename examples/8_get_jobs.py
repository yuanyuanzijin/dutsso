import sys
sys.path.append('.')
##################### 以上两行只是为了方便开发，实际不需要 #######################

import os
import time
import dutsso

# 查询招聘信息
date = "2018-03-15"
u = dutsso.User()
jobs = u.get_job(search_date=date)      # 如不填默认获取当天的
print("————%s招聘信息获取如下————" % date)
print(jobs)
