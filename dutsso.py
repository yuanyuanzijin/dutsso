import os
import json
import re
import requests
import urllib
from bs4 import BeautifulSoup
import execjs
import time
from operator import itemgetter

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import configparser


class User:
    def __init__(self, username='', password='', encrypted_password='', password_length=None):
        self.username = username
        self.password = password
        self.encrypted_password = encrypted_password
        self.password_length = password_length
        self.name = ""
        self.type = ""
        self.s = requests.Session()
    
    def __get_key(self, username, password, ticket):  
        ctx = execjs.compile(htmlstr)
        rsa = ctx.call('strEnc', username + password + ticket, '1', '2', '3')
        return rsa
    
    def get_encrypted_password(self):
        if self.password:
            encrypted_password = self.__get_key("", self.password, "")
            return encrypted_password
        else:
            eprint("密码未初始化，缺少password变量，无法执行此操作！")
            return False
      
    def cookies_get(self):
        cookies_list = []
        for c in self.s.cookies:
            c_dict = {
                'name': c.name,
                'value': c.value,
                'domain': c.domain,
                'path': c.path
            }
            cookies_list.append(c_dict)
        return cookies_list

    def cookies_save(self, cookies_list=None, path="cookies/"):
        if not cookies_list:
            cookies_list = self.cookies_get()
        if not os.path.exists(path):
            os.mkdir(path)
        filename = os.path.join(path, "cookies_dutsso_"+self.username+".coo")
        with open(filename, mode='w', encoding="utf-8") as f:
            f.write(json.dumps(cookies_list))
        return True

    def cookies_set(self, cookies_list):
        for c in cookies_list:
            self.s.cookies.set(c['name'], c['value'], path=c['path'], domain=c['domain'])
        return True

    def cookies_restore(self, path='cookies/'):
        filename = os.path.join(path, "cookies_dutsso_"+self.username+".coo")
        if os.path.exists(filename):
            with open(filename, mode='r', encoding="utf-8") as f:
                cookies_list = f.readline()
            try:    
                self.cookies_set(json.loads(cookies_list))
            except:
                iprint("登录状态恢复失败！")
                return False
            return True
        else:
            return False
    
    def login(self, try_cookies=True, try_rsa=True, auto_save=True, show_info=True):
        if not self.username:
            eprint("请初始化学号！")
        if try_cookies:
            result = self.cookies_restore()
            if result:
                iprint("尝试从Cookies中恢复登录状态...", show_info)
                if self.isactive():
                    try:
                        info = self.get_info()
                        self.name = info['name']
                        self.type = info['type']
                        iprint("已恢复登录状态！", show_info)
                        return True
                    except:
                        iprint("个人信息获取失败！")
                        return True
                else:
                    iprint("Cookies登录状态已失效！", show_info)
        
        self.s.cookies.clear()

        url = "https://sso.dlut.edu.cn/cas/login?service=http://portal.dlut.edu.cn/tp/"
        req = self.s.get(url, allow_redirects=False, timeout=30)
        soup = BeautifulSoup(req.text, 'html.parser')
        ticket = soup.select('#lt')[0]['value']
        execution = soup.select('input')[4]['value']

        if try_rsa and self.encrypted_password and self.password_length:
            iprint("正在使用密文密码登录...", show_info)
            rsa = self.__get_key(self.username, "", "") + self.encrypted_password + self.__get_key("", "", ticket)
            pl = self.password_length
        else:
            iprint("正在使用用户名密码登录...", show_info)
            rsa = self.__get_key(self.username, self.password, ticket)
            pl = len(self.password)
        ul = len(self.username)
        jsessionid = self.s.cookies['JSESSIONID']

        url2 = "https://sso.dlut.edu.cn/cas/login;jsessionid=%s?service=http://portal.dlut.edu.cn/tp/" % jsessionid
        data = {
            'rsa': rsa,
            'ul': ul,
            'pl': pl,
            'lt': ticket,
            'execution': execution,
            '_eventId': 'submit'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'            
        }
        req = self.s.post(url2, data=data, headers=headers, allow_redirects=False, timeout=30)
        soup = BeautifulSoup(req.text, 'html.parser')
        newaddr = soup.select('a')[0]['href']
        if newaddr.find("javascript") < 0:
            iprint("用户登录成功！", show_info)
            try:
                info = self.get_info()
                self.name = info['name']
                self.type = info['type']
            except:
                iprint("个人信息获取失败！")
            if auto_save:
                self.cookies_save()
                iprint("已自动保存登录信息！", show_info)
            return True
        else:
            iprint("用户登录失败！", show_info)
            return False
    
    def get_info(self):
        req = self.s.get('http://portal.dlut.edu.cn/tp/view?m=up')
        soup = BeautifulSoup(req.text, "html.parser")
        name = soup.select('#user-btn-01 span')[0].text
        url_info = 'https://portal.dlut.edu.cn/tp/sys/uacm/profile/getUserType'
        data = {}
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'http://portal.dlut.edu.cn',
            'Referer': 'http://portal.dlut.edu.cn/tp/view?m=up',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        }
        req = self.s.post(url_info, data=json.dumps(data), headers=headers)
        info_dict = json.loads(req.text)[0]
        info = {
            'type': info_dict['CODENAME'],
            'name': name
        }
        return info

    def get_all_info(self):
        req = self.s.get('http://portal.dlut.edu.cn/tp/view?m=up')
        url_info = 'https://portal.dlut.edu.cn/tp/sys/uacm/profile/get'
        data = {
            "ID_NUMBER": self.username,
            "mapping": "getUserById"
        }
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'http://portal.dlut.edu.cn',
            'Referer': 'http://portal.dlut.edu.cn/tp/view?m=up',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        }
        req = self.s.post(url_info, data=json.dumps(data), headers=headers)
        info_dict = json.loads(req.text)
        info = {
            'name': info_dict['USER_NAME'],
            'type': info_dict['ID_TYPE'],
            'depart': info_dict['UNIT_NAME'],
            'sex': info_dict['USER_SEX'],
            'home': info_dict['NATIVE_PLACE'],
            'mobile': info_dict['MOBILE'],
            'email': info_dict['EMAIL']
        }
        return info

    def get_card(self):
        url_card = "http://202.118.64.15/fabu/sso_jump.jsp"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'            
        }
        req = self.s.get(url_card, timeout=30, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        money = soup.select('#information td')[5].text.strip().strip("元")
        last_time = soup.select('#information td')[7].text.strip()
        info = {
            "money": money,
            "last_time": last_time
        }
        return info
    
    def get_bathroom(self):
        url_bathroom = "http://202.118.64.15/fabu/cardUserManager.do?method=queryTboxCount"
        req = self.s.get(url_bathroom, timeout=30)
        soup = BeautifulSoup(req.text, "html.parser")
        td = soup.select('.title tr td font')
        info = {
            'bs0': {
                'total': int(re.sub(r"\D", "", str(td[0]))),
                'use': int(re.sub(r"\D", "", str(td[1]))),
                'unuse': int(re.sub(r"\D", "", str(td[2])))  
            },
            'bs1': {
                'total': int(re.sub(r"\D", "", str(td[3]))),
                'use': int(re.sub(r"\D", "", str(td[4]))),
                'unuse': int(re.sub(r"\D", "", str(td[5])))
            },
            'xs0': {
                'total': int(re.sub(r"\D", "", str(td[6]))),
                'use': int(re.sub(r"\D", "", str(td[7]))),
                'unuse': int(re.sub(r"\D", "", str(td[8])))
            },
            'xs1': {
                'total': int(re.sub(r"\D", "", str(td[9]))),
                'use': int(re.sub(r"\D", "", str(td[10]))),
                'unuse': int(re.sub(r"\D", "", str(td[11])))
            },
        }
        return info


    def get_library(self):
        url = "http://portal.dlut.edu.cn/sso/sso_tsg.jsp"
        req = self.s.get(url, timeout=30)
        soup = BeautifulSoup(req.text, "html.parser")
        time = soup.select('form input')[1]['value']
        verify = soup.select('form input')[2]['value']
        
        url_lib_login = "http://opac.lib.dlut.edu.cn/reader/hwthau.php"
        data = {
            'un': self.username,
            'time': time,
            'verify': verify
        }
        req = self.s.post(url_lib_login, data=data, allow_redirects=False, timeout=30)
        
        url_lib_info = "http://opac.lib.dlut.edu.cn/reader/redr_info_rule.php"
        req = self.s.get(url_lib_info, timeout=30)
        soup = BeautifulSoup(req.content.decode('utf-8'), 'html.parser')
        myinfo = soup.select('#mylib_content table tr')
        try:
            borrow_times = myinfo[3].select('td')[2].text.strip("累计借书：").strip("册次")
            break_times = myinfo[4].select('td')[0].text.strip("违章次数：")
            break_money = myinfo[4].select('td')[1].text.strip("欠款金额：")
            bind_email = myinfo[5].select('td')[0].text.strip("Email：").strip()
            bind_phone = myinfo[7].select('td')[3].text.strip("手机：").strip()
            lib_dict = {
                "times": borrow_times,
                "break": break_times,
                "money": break_money,
                "email": bind_email,
                "phone": bind_phone
            }
            return lib_dict
        except:
            iprint("您的图书馆信息未激活，请登录图书馆后再试！")
            return False

    def get_network(self):
        req = self.s.get('https://portal.dlut.edu.cn/tp/view?m=up')
        url_info = 'https://portal.dlut.edu.cn/tp/up/subgroup/getTrafficList'
        data = {}
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'http://portal.dlut.edu.cn',
            'Referer': 'http://portal.dlut.edu.cn/tp/view?m=up',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        }
        req = self.s.post(url_info, data=json.dumps(data), headers=headers)
        info_dict = json.loads(req.text)[0]
        info = {
            'fee': info_dict['fee'],
            'used': info_dict['usedTraffic']
        }
        return info

    def get_email(self):
        req = self.s.get('https://portal.dlut.edu.cn/tp/view?m=up')
        url_info = 'https://portal.dlut.edu.cn/tp/up/subgroup/getUnReadList'
        data = {}
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'http://portal.dlut.edu.cn',
            'Referer': 'http://portal.dlut.edu.cn/tp/view?m=up',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        }
        req = self.s.post(url_info, data=json.dumps(data), headers=headers)
        info_dict = json.loads(req.text)
        info = {
            'email': info_dict['email'],
            'unread': info_dict['num']
        }
        return info

    def get_job(self, search_date=None):
        if not search_date:
            now = time.localtime(time.time())
            year = now.tm_year
            month = now.tm_mon
            day = now.tm_mday
            search_date = "%d-%02d-%d" % (year, month, day)
        job_url = "http://202.118.65.2/app/portals/recruiterNews?date=" + search_date
        jobs = json.loads(requests.get(job_url).text)
        jobs_list = []
        for i in jobs:
            i_url = "http://202.118.65.2/app/portals/newspage.html?id=" + i['id']
            detail = requests.get(i_url)
            soup = BeautifulSoup(detail.text, 'html.parser')
            th = soup.select('table th')
            try:
                i_addr = th[0].text.strip("场地地址：")
            except:
                i_addr = ""
            try:
                i_date = th[1].text.strip("日期：")
            except:
                i_date = ""
            try:
                i_time = th[2].text.strip("时间：")
            except:
                i_time = ""
            job_dict = {
                'title': i['title'],
                'url': i_url,
                'location': i_addr,
                'date': i_date,
                'time': i_time,
            }
            jobs_list.append(job_dict)
        jobs_list_sorted = sorted(jobs_list, key=itemgetter("date", "time"))
        return jobs_list_sorted

    def get_score_yjs(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'            
        }
        req = self.s.get('http://202.118.65.123/pyxx/grgl/xskccjcx.aspx?xh=%s' % self.username, timeout=30, allow_redirects=False, headers=headers)
        if req.status_code == 302:
            req = self.s.get("https://sso.dlut.edu.cn/cas/login?service=http://202.118.65.123/gmis/LoginCAS.aspx", timeout=30, headers=headers)
            req = self.s.get('http://202.118.65.123/pyxx/grgl/xskccjcx.aspx?xh=%s' % self.username, timeout=30)
        if req.status_code == 200:
            self.cookies_save()
        else:
            return False

        score_list = []
        soup = BeautifulSoup(req.text, 'html.parser')
        bx_scores = soup.select('#MainWork_dgData tr')[1:]
        for score in bx_scores:
            soup1 = BeautifulSoup(str(score), 'html.parser')
            c_name = soup1.select('td')[0].text
            c_score = soup1.select('td')[1].text
            try:
              c_value = soup1.select('span')[0].text
            except:
              c_value = "评价后查看"
            c_dict = {
                'c_name': c_name,
                'c_value': c_value,
                'c_score': c_score,
                'compulsory': True
            }
            score_list.append(c_dict)
        
        xx_scores = soup.select('#MainWork_Datagrid1 tr')[1:]
        for score in xx_scores:
            soup2 = BeautifulSoup(str(score), 'html.parser')
            c_name = soup2.select('td')[0].text
            c_score = soup2.select('td')[1].text
            try:
              c_value = soup2.select('span')[0].text
            except:
              c_value = "评价后查看"
            c_dict = {
                'c_name': c_name,
                'c_score': c_score,
                'c_value': c_value,
                'compulsory': False
            }
            score_list.append(c_dict)
        return score_list

    def get_plan_yjs(self):
        plan_yjs_url = 'http://202.118.65.123/pyxx/pygl/pyjhcx.aspx?xh=%s' % self.username
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'            
        }
        req = self.s.get(plan_yjs_url, timeout=30, allow_redirects=False, headers=headers)
        if req.status_code == 302:
            req = self.s.get("https://sso.dlut.edu.cn/cas/login?service=http://202.118.65.123/gmis/LoginCAS.aspx", timeout=30, headers=headers)
            req = self.s.get(plan_yjs_url, timeout=30, headers=headers)
        if req.status_code == 200:
            self.cookies_save()
        else:
            return False
            
        plan_list = []
        soup0 = BeautifulSoup(req.text, 'html.parser')
        plans = soup0.select('#MainWork_dgData tr')[1:]
        for plan in plans:
            soup = BeautifulSoup(str(plan), 'html.parser')
            tds = soup.select('td')
            p_name = tds[1].text.strip()
            p_type = tds[3].text.strip()
            compulsory = tds[4].text.strip()
            p_compulsory = True if compulsory == "是" else False
            p_score = tds[5].text.strip()
            p_time = tds[6].text.strip()
            p_term = tds[7].text.strip()
            p_dict = {
                'p_name': p_name,
                'p_type': p_type,
                'p_compulsory': p_compulsory,
                'p_score': p_score,
                'p_time': p_time,
                'p_term': p_term
            }
            plan_list.append(p_dict)
        
        plan_dict = {
            'plan': plan_list,
            'general': soup0.select('#MainWork_lbltitle')[0].text.strip(),
            'required': soup0.select('#MainWork_Label1')[0].text.strip(),
            'teacher': soup0.select('#MainWork_Label2')[0].text.strip(),
        }
        return plan_dict

    def get_course_yjs(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'            
        }
        url_course = "http://202.118.65.123/pyxx/pygl/pyjhxk.aspx?xh=" + self.username
        req = self.s.get(url_course, allow_redirects=False, headers=headers)
        if req.status_code == 302:
            req = self.s.get("https://sso.dlut.edu.cn/cas/login?service=http://202.118.65.123/gmis/LoginCAS.aspx", timeout=30, headers=headers)
            req = self.s.get(url_course, allow_redirects=False)
        if req.status_code == 200:
            self.cookies_save()
        else:
            return False

        soup = BeautifulSoup(req.text, "html.parser")
        tr_list = soup.select("#MainWork_dgData tr")[1:]
        course_list = []
        for index, tr in enumerate(tr_list):
            c_num = tr.select("td")[0].text.strip()
            c_address = tr.select("td")[1].text.strip()
            c_id = tr.select("td")[3].text.strip()
            c_name = tr.select("td")[4].text.strip()
            c_teacher = tr.select("td")[5].text.strip()
            c_time = tr.select("td")[6].text.strip()
            c_score = tr.select("td")[8].text.strip()
            c_whole = tr.select("td")[9].text.strip()
            full = tr.select("td")[10].text.strip()
            if full == "未满":
                c_full = False
            else:
                c_full = True
            method = tr.select("td")[11].text.strip()
            if method != "网上":
                continue
            choose = tr.select("td")[12].text.strip()
            if choose:
                c_choose = True
            else:
                c_choose = False
            pos = index + 2
            if pos < 10:
                c_position = '0' + str(pos)
            else:
                c_position = str(pos)
            action = choose = tr.select("td")[14].text.strip()
            if action:
                c_action = True
            else:
                c_action = False
            
            course_info = {
                'c_num': c_num,
                'c_address': c_address,
                'c_id': c_id,
                'c_name': c_name,
                'c_teacher': c_teacher,
                'c_time': c_time,
                'c_score': c_score,
                'c_whole': c_whole,
                'c_full': c_full,
                'c_choose': c_choose,
                'c_position': c_position,
                'c_action': c_action
            }
            course_list.append(course_info)
        return course_list
    
    def get_course_not_choosed_yjs(self, other_classes=False):
        course_list = self.get_course_yjs()
        course_list_not_choosed = []
        for i in course_list:
            # 包括未选的其他班级
            if other_classes:
                if not i['c_choose']:
                    course_list_not_choosed.append(i)
            # 忽略已选课程的其他班级
            else:
                if not i['c_choose'] and i['c_action']:
                    course_list_not_choosed.append(i)
        return course_list_not_choosed

    def get_course_choosed_yjs(self):
        course_list = self.get_course_yjs()
        course_list_choosed = []
        for i in course_list:
            if i['c_choose']:
                course_list_choosed.append(i)
        return course_list_choosed

    def choose_course_yjs(self, course_tr, method="choose", show_info=True):
        if method == "choose":
            if course_tr['c_choose']:
                iprint("您已选择%s，不需要重复选择" % course_tr['c_name'], show_info)
                return False
        elif method == "cancel":
            if not course_tr['c_choose']:
                iprint("您没有选择%s，不需要退课" % course_tr['c_name'], show_info)
                return False
        else:
            iprint("method参数错误！choose代表选课，cancel代表退课！", show_info)
            return False

        url_course = "http://202.118.65.123/pyxx/pygl/pyjhxk.aspx?xh=" + self.username
        req = self.s.get(url_course, allow_redirects=False)
        if req.status_code == 302:
            req = self.s.get("https://sso.dlut.edu.cn/cas/login?service=http://202.118.65.123/gmis/LoginCAS.aspx", timeout=30)
            req = self.s.get(url_course, allow_redirects=False)
        soup = BeautifulSoup(req.text, "html.parser")
        __VIEWSTATE = soup.select("#__VIEWSTATE")[0]['value']
        __VIEWSTATEGENERATOR = soup.select('#__VIEWSTATEGENERATOR')[0]['value']
        hftermCode = soup.select('#MainWork_hftermCode')[0]['value']
        
        if method == "choose":
            __EVENTTARGET = "ctl00$MainWork$dgData$ctl%s$Linkbutton2" % course_tr['c_position']
        elif method == "cancel":
            __EVENTTARGET = "ctl00$MainWork$dgData$ctl%s$LinkButton1" % course_tr['c_position']
        else:
            return False
        data = {
            "ctl00$ScriptManager1": "ctl00$MainWork$UpdatePanel|" + __EVENTTARGET,
            "__EVENTTARGET": __EVENTTARGET,
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": __VIEWSTATE,
            "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
            "ctl00$MainWork$hftermCode": hftermCode,
            "ctl00$MainWork$dropKeyword": 1,
            "ctl00$MainWork$txtKeyword": "",
            "__ASYNCPOST": True
        }
        headers = {
            "Referer": url_course,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "X-MicrosoftAjax": "Delta=true",
            "X-Requested-With": "XMLHttpRequest"
        }
        req = self.s.post(url_course, data=data, headers=headers)
        back = json.loads(req.text.split("|")[-2])["text"].split("'")
        if len(back) > 1:
            back = back[1]
        if back.find("成功") >= 0:
            return True
        else:
            iprint(back, show_info)
        return False

    def get_evaluate_list_yjs(self):
        url_evaluate_list = "http://202.118.65.123/pyxx/jxpj/jxpjlist.aspx?xh=" + self.username
        req = self.s.get(url_evaluate_list, allow_redirects=False)
        if req.status_code == 302:
            req = self.s.get("https://sso.dlut.edu.cn/cas/login?service=http://202.118.65.123/gmis/LoginCAS.aspx", timeout=30)
            req = self.s.get(url_evaluate_list, allow_redirects=False)
        if req.status_code == 200:
            self.cookies_save()
        else:
            return False

        evaluate_list = []
        soup = BeautifulSoup(req.text, "html.parser")
        list_tr = soup.select('#MainWork_dgData tr')[1:]
        for index, course in enumerate(list_tr):
            soup = BeautifulSoup(str(course), 'html.parser')
            tds = soup.select('td')
            e_name = tds[3].text.strip()
            e_teacher = tds[4].text.strip()
            e_complete = True if tds[5].text.strip() == "已参加" else False
            pos = index + 2
            if pos < 10:
                e_position = '0' + str(pos)
            else:
                e_position = str(pos)
            e_dict = {
                'e_name': e_name,
                'e_teacher': e_teacher,
                'e_complete': e_complete,
                'e_position': e_position
            }
            evaluate_list.append(e_dict)
        return evaluate_list

    def get_evaluate_list_unfinished_yjs(self):
        evaluate_list = self.get_evaluate_list_yjs()
        evaluate_list_unfinished = []
        for i in evaluate_list:
            if not i['e_complete']:
                evaluate_list_unfinished.append(i)
        return evaluate_list_unfinished
    
    def evaluate_course_yjs(self, evaluate_tr, choice_exam="A", choice_whole="A", remark_text="", rank=1):
        if not rank:
            rank = 1
        choice_list = ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd']
        if choice_exam not in choice_list:
            eprint("choice_exam代表考试方式，选项应为ABCD中的一项！A闭卷考试，B开卷考试，C大作业方式，D其他方式（不填默认为A）")
            return False
        
        if choice_whole not in choice_list:
            eprint("choice_whole代表总体评分，选项应为ABCD中的一项！（不填默认为A）")
            return False

        url_evaluate_list = "http://202.118.65.123/pyxx/jxpj/jxpjlist.aspx?xh=" + self.username
        req = self.s.get(url_evaluate_list, allow_redirects=False)
        if req.status_code == 302:
            req = self.s.get("https://sso.dlut.edu.cn/cas/login?service=http://202.118.65.123/gmis/LoginCAS.aspx", timeout=30)
            req = self.s.get(url_evaluate_list, allow_redirects=False)
        if req.status_code == 200:
            self.cookies_save()
        else:
            return False
        
        soup = BeautifulSoup(req.text, "html.parser")
        __VIEWSTATE = soup.select("#__VIEWSTATE")[0]['value']
        __VIEWSTATEGENERATOR = soup.select('#__VIEWSTATEGENERATOR')[0]['value']
        __EVENTTARGET = "ctl00$MainWork$dgData$ctl%s$Linkbutton1" % evaluate_tr['e_position']

        data = {
            "ctl00$ScriptManager1": "ctl00$MainWork$UpdatePanel|" + __EVENTTARGET,
            "__EVENTTARGET": __EVENTTARGET,
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": __VIEWSTATE,
            "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
            "ctl00$MainWork$hfxh": self.username,
            "__ASYNCPOST": True
        }
        headers = {
            "Referer": url_evaluate_list,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "X-MicrosoftAjax": "Delta=true",
            "X-Requested-With": "XMLHttpRequest"
        }
        req = self.s.post(url_evaluate_list, data=data, headers=headers)
        back = req.text.split("|")[-2]
        new_url = "http://202.118.65.123" + urllib.parse.unquote(back)
        e_id = int(new_url.split("=")[1].split("&")[0])
        iprint("成功获取到课程《%s》（评价编号：%d）的评价页面！正在评价中..." % (evaluate_tr['e_name'], e_id))
        req = self.s.get(new_url, allow_redirects=False, headers=headers)
        soup = BeautifulSoup(req.text, "html.parser")
        __VIEWSTATE = soup.select("#__VIEWSTATE")[0]['value']
        __VIEWSTATEGENERATOR = soup.select('#__VIEWSTATEGENERATOR')[0]['value']

        if choice_exam == "A" or choice_exam == "a":
            choice_exam_id = "rdoksfs_bjks"
        elif choice_exam == "B" or choice_exam == "b":
            choice_exam_id = "rdoksfs_kjks"
        elif choice_exam == "C" or choice_exam == "c":
            choice_exam_id = "rdoksfs_dzyfs"
        else:
            choice_exam_id = "rdoksfs_qtfs"

        if choice_whole == "A" or choice_whole == "a":
            choice_whole_id = 322
        elif choice_whole == "B" or choice_whole == "b":
            choice_whole_id = 323
        elif choice_whole == "C" or choice_whole == "c":
            choice_whole_id = 324
        else:
            choice_whole_id = 325

        data = {
            "ctl00$ScriptManager1": "ctl00$MainWork$UpdatePanel|ctl00$MainWork$cmdAdd",
            "__EVENTTARGET": "ctl00$MainWork$cmdAdd",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": __VIEWSTATE,
            "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
            "ctl00$MainWork$hfxh": self.username,
            "ctl00$MainWork$hfpjid": e_id,
            "ctl00$MainWork$ksfs": choice_exam_id,
            "ctl00$MainWork$zyskfs": "rdozyskfs_ktsk",
            "ctl00$MainWork$dltm_jxtd$ctl00$radlda": 261,
            "ctl00$MainWork$dltm_jxtd$ctl01$radlda": 264,
            "ctl00$MainWork$dltm_jxtd$ctl02$radlda": 267,
            "ctl00$MainWork$dltm_jxtd$ctl03$radlda": 271,
            "ctl00$MainWork$dltm_jxtd$ctl04$radlda": 276,
            "ctl00$MainWork$dltm_jxtd$ctl05$radlda": 280,
            "ctl00$MainWork$dltm_jxnr$ctl00$radlda": 284,
            "ctl00$MainWork$dltm_jxnr$ctl01$radlda": 286,
            "ctl00$MainWork$dltm_jxnr$ctl02$radlda": 290,
            "ctl00$MainWork$dltm_jxff$ctl00$radlda": 294,
            "ctl00$MainWork$dltm_jxff$ctl01$radlda": 298,
            "ctl00$MainWork$dltm_jxff$ctl02$radlda": 302,
            "ctl00$MainWork$dltm_jxff$ctl03$radlda": 306,
            "ctl00$MainWork$dltm_jxxg$ctl00$radlda": 310,
            "ctl00$MainWork$dltm_jxxg$ctl01$radlda": 314,
            "ctl00$MainWork$dltm_jxxg$ctl02$radlda": 318,
            "ctl00$MainWork$txtbz": remark_text,
            "ctl00$MainWork$radlztpj": choice_whole_id,
            "ctl00$MainWork$txtrkjspm": rank,
            "__ASYNCPOST": True
        }
        headers = {
            "Referer": new_url,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "X-MicrosoftAjax": "Delta=true",
            "X-Requested-With": "XMLHttpRequest"
        }
        req = self.s.post(new_url, data=data, headers=headers)
        info = req.text.split("alert")[1].split("|")[0].split("\\u0027")[1]
        if info == "提交成功！":
            return True
        else:
            iprint(info)
            return False

    def logout(self, clear_save=False, path="./"):
        self.s.cookies.clear()
        if clear_save:
            filename = os.path.join(path, "cookies_dutsso_"+self.username+".coo")
            if os.path.exists(filename):
                os.remove(filename)
                return
        return

    def isactive(self):
        headers = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        }
        req = self.s.get("https://portal.dlut.edu.cn/tp/view?m=up", allow_redirects=False, timeout=30, headers=headers)
        if req.status_code == 200:
            return True
        else:
            return False


class Mail:
    def __init__(self):
        self.init_finished = False

    def init_from_file(self, config_path=None):
        if config_path == None:
            root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
            config_path = os.path.join(root_path, "mail_config.ini")

        if not os.path.exists(config_path):
            eprint("请检查配置文件的路径！并请确保已将项目中的mail_config.ini.example重命名为mail_config.ini")
            return False

        c = configparser.ConfigParser()
        try:
            with open(config_path) as f:
                c.readfp(f)
                self.mail_host = c.get('info', 'mail_host')
                self.mail_port = c.get('info', 'mail_port')
                self.mail_user = c.get('info', 'mail_user')
                self.mail_pass = c.get('info', 'mail_pass')
                self.sender = c.get('info', 'sender')
            self.init_finished = True
            return True
        except:
            eprint("mail_config.ini配置文件格式有误，请检查重试！")
            self.init_finished = False
            return False

    def send(self, mailto, subject, content):
        if not self.init_finished:
            eprint("请先使用init_from_file方法初始化邮件配置！")
            return False

        if type(mailto) == str:
            receivers = [mailto]
        else:
            receivers = mailto
        mail_msg = content
        m = MIMEText(mail_msg, 'html', 'utf-8')
        m['From'] = self.sender
        m['To'] = ";".join(receivers)
        m['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP_SSL()
            smtpObj.connect(self.mail_host, self.mail_port)
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(self.sender, receivers, m.as_string())
            return True
        except smtplib.SMTPException:
            return False

def iprint(info, show_info=True):
    if show_info:
          print("Info: " + info)

def eprint(info):
    print("Error: " + info)







htmlstr = '''
function strEnc(data,firstKey,secondKey,thirdKey){  
  
 var leng = data.length;  
 var encData = "";  
 var firstKeyBt,secondKeyBt,thirdKeyBt,firstLength,secondLength,thirdLength;  
 if(firstKey != null && firstKey != ""){      
   firstKeyBt = getKeyBytes(firstKey);  
   firstLength = firstKeyBt.length;  
 }  
 if(secondKey != null && secondKey != ""){  
   secondKeyBt = getKeyBytes(secondKey);  
   secondLength = secondKeyBt.length;  
 }  
 if(thirdKey != null && thirdKey != ""){  
   thirdKeyBt = getKeyBytes(thirdKey);  
   thirdLength = thirdKeyBt.length;  
 }    
   
 if(leng > 0){  
   if(leng < 4){  
     var bt = strToBt(data);        
     var encByte ;  
     if(firstKey != null && firstKey !="" && secondKey != null && secondKey != "" && thirdKey != null && thirdKey != ""){  
       var tempBt;  
       var x,y,z;  
       tempBt = bt;          
       for(x = 0;x < firstLength ;x ++){  
         tempBt = enc(tempBt,firstKeyBt[x]);  
       }  
       for(y = 0;y < secondLength ;y ++){  
         tempBt = enc(tempBt,secondKeyBt[y]);  
       }  
       for(z = 0;z < thirdLength ;z ++){  
         tempBt = enc(tempBt,thirdKeyBt[z]);  
       }          
       encByte = tempBt;          
     }else{  
       if(firstKey != null && firstKey !="" && secondKey != null && secondKey != ""){  
         var tempBt;  
         var x,y;  
         tempBt = bt;  
         for(x = 0;x < firstLength ;x ++){  
           tempBt = enc(tempBt,firstKeyBt[x]);  
         }  
         for(y = 0;y < secondLength ;y ++){  
           tempBt = enc(tempBt,secondKeyBt[y]);  
         }  
         encByte = tempBt;  
       }else{  
         if(firstKey != null && firstKey !=""){              
           var tempBt;  
           var x = 0;  
           tempBt = bt;              
           for(x = 0;x < firstLength ;x ++){  
             tempBt = enc(tempBt,firstKeyBt[x]);  
           }  
           encByte = tempBt;  
         }  
       }          
     }  
     encData = bt64ToHex(encByte);  
   }else{  
     var iterator = parseInt(leng/4);  
     var remainder = leng%4;  
     var i=0;        
     for(i = 0;i < iterator;i++){  
       var tempData = data.substring(i*4+0,i*4+4);  
       var tempByte = strToBt(tempData);  
       var encByte ;  
       if(firstKey != null && firstKey !="" && secondKey != null && secondKey != "" && thirdKey != null && thirdKey != ""){  
         var tempBt;  
         var x,y,z;  
         tempBt = tempByte;  
         for(x = 0;x < firstLength ;x ++){  
           tempBt = enc(tempBt,firstKeyBt[x]);  
         }  
         for(y = 0;y < secondLength ;y ++){  
           tempBt = enc(tempBt,secondKeyBt[y]);  
         }  
         for(z = 0;z < thirdLength ;z ++){  
           tempBt = enc(tempBt,thirdKeyBt[z]);  
         }  
         encByte = tempBt;  
       }else{  
         if(firstKey != null && firstKey !="" && secondKey != null && secondKey != ""){  
           var tempBt;  
           var x,y;  
           tempBt = tempByte;  
           for(x = 0;x < firstLength ;x ++){  
             tempBt = enc(tempBt,firstKeyBt[x]);  
           }  
           for(y = 0;y < secondLength ;y ++){  
             tempBt = enc(tempBt,secondKeyBt[y]);  
           }  
           encByte = tempBt;  
         }else{  
           if(firstKey != null && firstKey !=""){                        
             var tempBt;  
             var x;  
             tempBt = tempByte;  
             for(x = 0;x < firstLength ;x ++){                  
               tempBt = enc(tempBt,firstKeyBt[x]);  
             }  
             encByte = tempBt;                
           }  
         }  
       }  
       encData += bt64ToHex(encByte);  
     }        
     if(remainder > 0){  
       var remainderData = data.substring(iterator*4+0,leng);  
       var tempByte = strToBt(remainderData);  
       var encByte ;  
       if(firstKey != null && firstKey !="" && secondKey != null && secondKey != "" && thirdKey != null && thirdKey != ""){  
         var tempBt;  
         var x,y,z;  
         tempBt = tempByte;  
         for(x = 0;x < firstLength ;x ++){  
           tempBt = enc(tempBt,firstKeyBt[x]);  
         }  
         for(y = 0;y < secondLength ;y ++){  
           tempBt = enc(tempBt,secondKeyBt[y]);  
         }  
         for(z = 0;z < thirdLength ;z ++){  
           tempBt = enc(tempBt,thirdKeyBt[z]);  
         }  
         encByte = tempBt;  
       }else{  
         if(firstKey != null && firstKey !="" && secondKey != null && secondKey != ""){  
           var tempBt;  
           var x,y;  
           tempBt = tempByte;  
           for(x = 0;x < firstLength ;x ++){  
             tempBt = enc(tempBt,firstKeyBt[x]);  
           }  
           for(y = 0;y < secondLength ;y ++){  
             tempBt = enc(tempBt,secondKeyBt[y]);  
           }  
           encByte = tempBt;  
         }else{  
           if(firstKey != null && firstKey !=""){              
             var tempBt;  
             var x;  
             tempBt = tempByte;  
             for(x = 0;x < firstLength ;x ++){  
               tempBt = enc(tempBt,firstKeyBt[x]);  
             }  
             encByte = tempBt;  
           }  
         }  
       }  
       encData += bt64ToHex(encByte);  
     }                  
   }  
 }  
 return encData;  
}  
  
/* 
* decrypt the encrypted string to the original string  
* 
* return  the original string   
*/  
function strDec(data,firstKey,secondKey,thirdKey){  
 var leng = data.length;  
 var decStr = "";  
 var firstKeyBt,secondKeyBt,thirdKeyBt,firstLength,secondLength,thirdLength;  
 if(firstKey != null && firstKey != ""){      
   firstKeyBt = getKeyBytes(firstKey);  
   firstLength = firstKeyBt.length;  
 }  
 if(secondKey != null && secondKey != ""){  
   secondKeyBt = getKeyBytes(secondKey);  
   secondLength = secondKeyBt.length;  
 }  
 if(thirdKey != null && thirdKey != ""){  
   thirdKeyBt = getKeyBytes(thirdKey);  
   thirdLength = thirdKeyBt.length;  
 }  
   
 var iterator = parseInt(leng/16);  
 var i=0;    
 for(i = 0;i < iterator;i++){  
   var tempData = data.substring(i*16+0,i*16+16);      
   var strByte = hexToBt64(tempData);      
   var intByte = new Array(64);  
   var j = 0;  
   for(j = 0;j < 64; j++){  
     intByte[j] = parseInt(strByte.substring(j,j+1));  
   }      
   var decByte;  
   if(firstKey != null && firstKey !="" && secondKey != null && secondKey != "" && thirdKey != null && thirdKey != ""){  
     var tempBt;  
     var x,y,z;  
     tempBt = intByte;  
     for(x = thirdLength - 1;x >= 0;x --){  
       tempBt = dec(tempBt,thirdKeyBt[x]);  
     }  
     for(y = secondLength - 1;y >= 0;y --){  
       tempBt = dec(tempBt,secondKeyBt[y]);  
     }  
     for(z = firstLength - 1;z >= 0 ;z --){  
       tempBt = dec(tempBt,firstKeyBt[z]);  
     }  
     decByte = tempBt;  
   }else{  
     if(firstKey != null && firstKey !="" && secondKey != null && secondKey != ""){  
       var tempBt;  
       var x,y,z;  
       tempBt = intByte;  
       for(x = secondLength - 1;x >= 0 ;x --){  
         tempBt = dec(tempBt,secondKeyBt[x]);  
       }  
       for(y = firstLength - 1;y >= 0 ;y --){  
         tempBt = dec(tempBt,firstKeyBt[y]);  
       }  
       decByte = tempBt;  
     }else{  
       if(firstKey != null && firstKey !=""){  
         var tempBt;  
         var x,y,z;  
         tempBt = intByte;  
         for(x = firstLength - 1;x >= 0 ;x --){  
           tempBt = dec(tempBt,firstKeyBt[x]);  
         }  
         decByte = tempBt;  
       }  
     }  
   }  
   decStr += byteToString(decByte);  
 }        
 return decStr;  
}  
/* 
* chang the string into the bit array 
*  
* return bit array(it's length % 64 = 0) 
*/  
function getKeyBytes(key){  
 var keyBytes = new Array();  
 var leng = key.length;  
 var iterator = parseInt(leng/4);  
 var remainder = leng%4;  
 var i = 0;  
 for(i = 0;i < iterator; i ++){  
   keyBytes[i] = strToBt(key.substring(i*4+0,i*4+4));  
 }  
 if(remainder > 0){  
   keyBytes[i] = strToBt(key.substring(i*4+0,leng));  
 }      
 return keyBytes;  
}  
  
/* 
* chang the string(it's length <= 4) into the bit array 
*  
* return bit array(it's length = 64) 
*/  
function strToBt(str){    
 var leng = str.length;  
 var bt = new Array(64);  
 if(leng < 4){  
   var i=0,j=0,p=0,q=0;  
   for(i = 0;i<leng;i++){  
     var k = str.charCodeAt(i);  
     for(j=0;j<16;j++){        
       var pow=1,m=0;  
       for(m=15;m>j;m--){  
         pow *= 2;  
       }          
       bt[16*i+j]=parseInt(k/pow)%2;  
     }  
   }  
   for(p = leng;p<4;p++){  
     var k = 0;  
     for(q=0;q<16;q++){        
       var pow=1,m=0;  
       for(m=15;m>q;m--){  
         pow *= 2;  
       }          
       bt[16*p+q]=parseInt(k/pow)%2;  
     }  
   }    
 }else{  
   for(i = 0;i<4;i++){  
     var k = str.charCodeAt(i);  
     for(j=0;j<16;j++){        
       var pow=1;  
       for(m=15;m>j;m--){  
         pow *= 2;  
       }          
       bt[16*i+j]=parseInt(k/pow)%2;  
     }  
   }    
 }  
 return bt;  
}  
  
/* 
* chang the bit(it's length = 4) into the hex 
*  
* return hex 
*/  
function bt4ToHex(binary) {  
 var hex;  
 switch (binary) {  
   case "0000" : hex = "0"; break;  
   case "0001" : hex = "1"; break;  
   case "0010" : hex = "2"; break;  
   case "0011" : hex = "3"; break;  
   case "0100" : hex = "4"; break;  
   case "0101" : hex = "5"; break;  
   case "0110" : hex = "6"; break;  
   case "0111" : hex = "7"; break;  
   case "1000" : hex = "8"; break;  
   case "1001" : hex = "9"; break;  
   case "1010" : hex = "A"; break;  
   case "1011" : hex = "B"; break;  
   case "1100" : hex = "C"; break;  
   case "1101" : hex = "D"; break;  
   case "1110" : hex = "E"; break;  
   case "1111" : hex = "F"; break;  
 }  
 return hex;  
}  
  
/* 
* chang the hex into the bit(it's length = 4) 
*  
* return the bit(it's length = 4) 
*/  
function hexToBt4(hex) {  
 var binary;  
 switch (hex) {  
   case "0" : binary = "0000"; break;  
   case "1" : binary = "0001"; break;  
   case "2" : binary = "0010"; break;  
   case "3" : binary = "0011"; break;  
   case "4" : binary = "0100"; break;  
   case "5" : binary = "0101"; break;  
   case "6" : binary = "0110"; break;  
   case "7" : binary = "0111"; break;  
   case "8" : binary = "1000"; break;  
   case "9" : binary = "1001"; break;  
   case "A" : binary = "1010"; break;  
   case "B" : binary = "1011"; break;  
   case "C" : binary = "1100"; break;  
   case "D" : binary = "1101"; break;  
   case "E" : binary = "1110"; break;  
   case "F" : binary = "1111"; break;  
 }  
 return binary;  
}  
  
/* 
* chang the bit(it's length = 64) into the string 
*  
* return string 
*/  
function byteToString(byteData){  
 var str="";  
 for(i = 0;i<4;i++){  
   var count=0;  
   for(j=0;j<16;j++){          
     var pow=1;  
     for(m=15;m>j;m--){  
       pow*=2;  
     }                
     count+=byteData[16*i+j]*pow;  
   }          
   if(count != 0){  
     str+=String.fromCharCode(count);  
   }  
 }  
 return str;  
}  
  
function bt64ToHex(byteData){  
 var hex = "";  
 for(i = 0;i<16;i++){  
   var bt = "";  
   for(j=0;j<4;j++){      
     bt += byteData[i*4+j];  
   }      
   hex+=bt4ToHex(bt);  
 }  
 return hex;  
}  
  
function hexToBt64(hex){  
 var binary = "";  
 for(i = 0;i<16;i++){  
   binary+=hexToBt4(hex.substring(i,i+1));  
 }  
 return binary;  
}  
  
/* 
* the 64 bit des core arithmetic 
*/  
  
function enc(dataByte,keyByte){    
 var keys = generateKeys(keyByte);      
 var ipByte   = initPermute(dataByte);    
 var ipLeft   = new Array(32);  
 var ipRight  = new Array(32);  
 var tempLeft = new Array(32);  
 var i = 0,j = 0,k = 0,m = 0, n = 0;  
 for(k = 0;k < 32;k ++){  
   ipLeft[k] = ipByte[k];  
   ipRight[k] = ipByte[32+k];  
 }      
 for(i = 0;i < 16;i ++){  
   for(j = 0;j < 32;j ++){  
     tempLeft[j] = ipLeft[j];  
     ipLeft[j] = ipRight[j];        
   }    
   var key = new Array(48);  
   for(m = 0;m < 48;m ++){  
     key[m] = keys[i][m];  
   }  
   var  tempRight = xor(pPermute(sBoxPermute(xor(expandPermute(ipRight),key))), tempLeft);        
   for(n = 0;n < 32;n ++){  
     ipRight[n] = tempRight[n];  
   }    
     
 }    
   
   
 var finalData =new Array(64);  
 for(i = 0;i < 32;i ++){  
   finalData[i] = ipRight[i];  
   finalData[32+i] = ipLeft[i];  
 }  
 return finallyPermute(finalData);    
}  
  
function dec(dataByte,keyByte){    
 var keys = generateKeys(keyByte);      
 var ipByte   = initPermute(dataByte);    
 var ipLeft   = new Array(32);  
 var ipRight  = new Array(32);  
 var tempLeft = new Array(32);  
 var i = 0,j = 0,k = 0,m = 0, n = 0;  
 for(k = 0;k < 32;k ++){  
   ipLeft[k] = ipByte[k];  
   ipRight[k] = ipByte[32+k];  
 }    
 for(i = 15;i >= 0;i --){  
   for(j = 0;j < 32;j ++){  
     tempLeft[j] = ipLeft[j];  
     ipLeft[j] = ipRight[j];        
   }    
   var key = new Array(48);  
   for(m = 0;m < 48;m ++){  
     key[m] = keys[i][m];  
   }  
     
   var  tempRight = xor(pPermute(sBoxPermute(xor(expandPermute(ipRight),key))), tempLeft);        
   for(n = 0;n < 32;n ++){  
     ipRight[n] = tempRight[n];  
   }    
 }    
   
   
 var finalData =new Array(64);  
 for(i = 0;i < 32;i ++){  
   finalData[i] = ipRight[i];  
   finalData[32+i] = ipLeft[i];  
 }  
 return finallyPermute(finalData);    
}  
  
function initPermute(originalData){  
 var ipByte = new Array(64);  
 for (i = 0, m = 1, n = 0; i < 4; i++, m += 2, n += 2) {  
   for (j = 7, k = 0; j >= 0; j--, k++) {  
     ipByte[i * 8 + k] = originalData[j * 8 + m];  
     ipByte[i * 8 + k + 32] = originalData[j * 8 + n];  
   }  
 }      
 return ipByte;  
}  
  
function expandPermute(rightData){    
 var epByte = new Array(48);  
 for (i = 0; i < 8; i++) {  
   if (i == 0) {  
     epByte[i * 6 + 0] = rightData[31];  
   } else {  
     epByte[i * 6 + 0] = rightData[i * 4 - 1];  
   }  
   epByte[i * 6 + 1] = rightData[i * 4 + 0];  
   epByte[i * 6 + 2] = rightData[i * 4 + 1];  
   epByte[i * 6 + 3] = rightData[i * 4 + 2];  
   epByte[i * 6 + 4] = rightData[i * 4 + 3];  
   if (i == 7) {  
     epByte[i * 6 + 5] = rightData[0];  
   } else {  
     epByte[i * 6 + 5] = rightData[i * 4 + 4];  
   }  
 }        
 return epByte;  
}  
  
function xor(byteOne,byteTwo){    
 var xorByte = new Array(byteOne.length);  
 for(i = 0;i < byteOne.length; i ++){        
   xorByte[i] = byteOne[i] ^ byteTwo[i];  
 }    
 return xorByte;  
}  
  
function sBoxPermute(expandByte){  
   
   var sBoxByte = new Array(32);  
   var binary = "";  
   var s1 = [  
       [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],  
       [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],  
       [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],  
       [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13 ]];  
  
       /* Table - s2 */  
   var s2 = [  
       [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],  
       [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],  
       [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],  
       [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9 ]];  
  
       /* Table - s3 */  
   var s3= [  
       [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],  
       [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],  
       [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],  
       [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12 ]];  
       /* Table - s4 */  
   var s4 = [  
       [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],  
       [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],  
       [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],  
       [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14 ]];  
  
       /* Table - s5 */  
   var s5 = [  
       [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],  
       [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],  
       [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],  
       [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3 ]];  
  
       /* Table - s6 */  
   var s6 = [  
       [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],  
       [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],  
       [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],  
       [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13 ]];  
  
       /* Table - s7 */  
   var s7 = [  
       [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],  
       [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],  
       [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],  
       [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]];  
  
       /* Table - s8 */  
   var s8 = [  
       [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],  
       [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],  
       [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],  
       [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]];  
     
   for(m=0;m<8;m++){  
   var i=0,j=0;  
   i = expandByte[m*6+0]*2+expandByte[m*6+5];  
   j = expandByte[m * 6 + 1] * 2 * 2 * 2   
     + expandByte[m * 6 + 2] * 2* 2   
     + expandByte[m * 6 + 3] * 2   
     + expandByte[m * 6 + 4];  
   switch (m) {  
     case 0 :  
       binary = getBoxBinary(s1[i][j]);  
       break;  
     case 1 :  
       binary = getBoxBinary(s2[i][j]);  
       break;  
     case 2 :  
       binary = getBoxBinary(s3[i][j]);  
       break;  
     case 3 :  
       binary = getBoxBinary(s4[i][j]);  
       break;  
     case 4 :  
       binary = getBoxBinary(s5[i][j]);  
       break;  
     case 5 :  
       binary = getBoxBinary(s6[i][j]);  
       break;  
     case 6 :  
       binary = getBoxBinary(s7[i][j]);  
       break;  
     case 7 :  
       binary = getBoxBinary(s8[i][j]);  
       break;  
   }        
   sBoxByte[m*4+0] = parseInt(binary.substring(0,1));  
   sBoxByte[m*4+1] = parseInt(binary.substring(1,2));  
   sBoxByte[m*4+2] = parseInt(binary.substring(2,3));  
   sBoxByte[m*4+3] = parseInt(binary.substring(3,4));  
 }  
 return sBoxByte;  
}  
  
function pPermute(sBoxByte){  
 var pBoxPermute = new Array(32);  
 pBoxPermute[ 0] = sBoxByte[15];   
 pBoxPermute[ 1] = sBoxByte[ 6];   
 pBoxPermute[ 2] = sBoxByte[19];   
 pBoxPermute[ 3] = sBoxByte[20];   
 pBoxPermute[ 4] = sBoxByte[28];   
 pBoxPermute[ 5] = sBoxByte[11];   
 pBoxPermute[ 6] = sBoxByte[27];   
 pBoxPermute[ 7] = sBoxByte[16];   
 pBoxPermute[ 8] = sBoxByte[ 0];   
 pBoxPermute[ 9] = sBoxByte[14];   
 pBoxPermute[10] = sBoxByte[22];   
 pBoxPermute[11] = sBoxByte[25];   
 pBoxPermute[12] = sBoxByte[ 4];   
 pBoxPermute[13] = sBoxByte[17];   
 pBoxPermute[14] = sBoxByte[30];   
 pBoxPermute[15] = sBoxByte[ 9];   
 pBoxPermute[16] = sBoxByte[ 1];   
 pBoxPermute[17] = sBoxByte[ 7];   
 pBoxPermute[18] = sBoxByte[23];   
 pBoxPermute[19] = sBoxByte[13];   
 pBoxPermute[20] = sBoxByte[31];   
 pBoxPermute[21] = sBoxByte[26];   
 pBoxPermute[22] = sBoxByte[ 2];   
 pBoxPermute[23] = sBoxByte[ 8];   
 pBoxPermute[24] = sBoxByte[18];   
 pBoxPermute[25] = sBoxByte[12];   
 pBoxPermute[26] = sBoxByte[29];   
 pBoxPermute[27] = sBoxByte[ 5];   
 pBoxPermute[28] = sBoxByte[21];   
 pBoxPermute[29] = sBoxByte[10];   
 pBoxPermute[30] = sBoxByte[ 3];   
 pBoxPermute[31] = sBoxByte[24];      
 return pBoxPermute;  
}  
  
function finallyPermute(endByte){      
 var fpByte = new Array(64);    
 fpByte[ 0] = endByte[39];   
 fpByte[ 1] = endByte[ 7];   
 fpByte[ 2] = endByte[47];   
 fpByte[ 3] = endByte[15];   
 fpByte[ 4] = endByte[55];   
 fpByte[ 5] = endByte[23];   
 fpByte[ 6] = endByte[63];   
 fpByte[ 7] = endByte[31];   
 fpByte[ 8] = endByte[38];   
 fpByte[ 9] = endByte[ 6];   
 fpByte[10] = endByte[46];   
 fpByte[11] = endByte[14];   
 fpByte[12] = endByte[54];   
 fpByte[13] = endByte[22];   
 fpByte[14] = endByte[62];   
 fpByte[15] = endByte[30];   
 fpByte[16] = endByte[37];   
 fpByte[17] = endByte[ 5];   
 fpByte[18] = endByte[45];   
 fpByte[19] = endByte[13];   
 fpByte[20] = endByte[53];   
 fpByte[21] = endByte[21];   
 fpByte[22] = endByte[61];   
 fpByte[23] = endByte[29];   
 fpByte[24] = endByte[36];   
 fpByte[25] = endByte[ 4];   
 fpByte[26] = endByte[44];   
 fpByte[27] = endByte[12];   
 fpByte[28] = endByte[52];   
 fpByte[29] = endByte[20];   
 fpByte[30] = endByte[60];   
 fpByte[31] = endByte[28];   
 fpByte[32] = endByte[35];   
 fpByte[33] = endByte[ 3];   
 fpByte[34] = endByte[43];   
 fpByte[35] = endByte[11];   
 fpByte[36] = endByte[51];   
 fpByte[37] = endByte[19];   
 fpByte[38] = endByte[59];   
 fpByte[39] = endByte[27];   
 fpByte[40] = endByte[34];   
 fpByte[41] = endByte[ 2];   
 fpByte[42] = endByte[42];   
 fpByte[43] = endByte[10];   
 fpByte[44] = endByte[50];   
 fpByte[45] = endByte[18];   
 fpByte[46] = endByte[58];   
 fpByte[47] = endByte[26];   
 fpByte[48] = endByte[33];   
 fpByte[49] = endByte[ 1];   
 fpByte[50] = endByte[41];   
 fpByte[51] = endByte[ 9];   
 fpByte[52] = endByte[49];   
 fpByte[53] = endByte[17];   
 fpByte[54] = endByte[57];   
 fpByte[55] = endByte[25];   
 fpByte[56] = endByte[32];   
 fpByte[57] = endByte[ 0];   
 fpByte[58] = endByte[40];   
 fpByte[59] = endByte[ 8];   
 fpByte[60] = endByte[48];   
 fpByte[61] = endByte[16];   
 fpByte[62] = endByte[56];   
 fpByte[63] = endByte[24];  
 return fpByte;  
}  
  
function getBoxBinary(i) {  
 var binary = "";  
 switch (i) {  
   case 0 :binary = "0000";break;  
   case 1 :binary = "0001";break;  
   case 2 :binary = "0010";break;  
   case 3 :binary = "0011";break;  
   case 4 :binary = "0100";break;  
   case 5 :binary = "0101";break;  
   case 6 :binary = "0110";break;  
   case 7 :binary = "0111";break;  
   case 8 :binary = "1000";break;  
   case 9 :binary = "1001";break;  
   case 10 :binary = "1010";break;  
   case 11 :binary = "1011";break;  
   case 12 :binary = "1100";break;  
   case 13 :binary = "1101";break;  
   case 14 :binary = "1110";break;  
   case 15 :binary = "1111";break;  
 }  
 return binary;  
}  
/* 
* generate 16 keys for xor 
* 
*/  
function generateKeys(keyByte){      
 var key   = new Array(56);  
 var keys = new Array();    
   
 keys[ 0] = new Array();  
 keys[ 1] = new Array();  
 keys[ 2] = new Array();  
 keys[ 3] = new Array();  
 keys[ 4] = new Array();  
 keys[ 5] = new Array();  
 keys[ 6] = new Array();  
 keys[ 7] = new Array();  
 keys[ 8] = new Array();  
 keys[ 9] = new Array();  
 keys[10] = new Array();  
 keys[11] = new Array();  
 keys[12] = new Array();  
 keys[13] = new Array();  
 keys[14] = new Array();  
 keys[15] = new Array();    
 var loop = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1];  
  
 for(i=0;i<7;i++){  
   for(j=0,k=7;j<8;j++,k--){  
     key[i*8+j]=keyByte[8*k+i];  
   }  
 }      
   
 var i = 0;  
 for(i = 0;i < 16;i ++){  
   var tempLeft=0;  
   var tempRight=0;  
   for(j = 0; j < loop[i];j ++){            
     tempLeft = key[0];  
     tempRight = key[28];  
     for(k = 0;k < 27 ;k ++){  
       key[k] = key[k+1];  
       key[28+k] = key[29+k];  
     }    
     key[27]=tempLeft;  
     key[55]=tempRight;  
   }  
   var tempKey = new Array(48);  
   tempKey[ 0] = key[13];  
   tempKey[ 1] = key[16];  
   tempKey[ 2] = key[10];  
   tempKey[ 3] = key[23];  
   tempKey[ 4] = key[ 0];  
   tempKey[ 5] = key[ 4];  
   tempKey[ 6] = key[ 2];  
   tempKey[ 7] = key[27];  
   tempKey[ 8] = key[14];  
   tempKey[ 9] = key[ 5];  
   tempKey[10] = key[20];  
   tempKey[11] = key[ 9];  
   tempKey[12] = key[22];  
   tempKey[13] = key[18];  
   tempKey[14] = key[11];  
   tempKey[15] = key[ 3];  
   tempKey[16] = key[25];  
   tempKey[17] = key[ 7];  
   tempKey[18] = key[15];  
   tempKey[19] = key[ 6];  
   tempKey[20] = key[26];  
   tempKey[21] = key[19];  
   tempKey[22] = key[12];  
   tempKey[23] = key[ 1];  
   tempKey[24] = key[40];  
   tempKey[25] = key[51];  
   tempKey[26] = key[30];  
   tempKey[27] = key[36];  
   tempKey[28] = key[46];  
   tempKey[29] = key[54];  
   tempKey[30] = key[29];  
   tempKey[31] = key[39];  
   tempKey[32] = key[50];  
   tempKey[33] = key[44];  
   tempKey[34] = key[32];  
   tempKey[35] = key[47];  
   tempKey[36] = key[43];  
   tempKey[37] = key[48];  
   tempKey[38] = key[38];  
   tempKey[39] = key[55];  
   tempKey[40] = key[33];  
   tempKey[41] = key[52];  
   tempKey[42] = key[45];  
   tempKey[43] = key[41];  
   tempKey[44] = key[49];  
   tempKey[45] = key[35];  
   tempKey[46] = key[28];  
   tempKey[47] = key[31];  
   switch(i){  
     case 0: for(m=0;m < 48 ;m++){ keys[ 0][m] = tempKey[m]; } break;  
     case 1: for(m=0;m < 48 ;m++){ keys[ 1][m] = tempKey[m]; } break;  
     case 2: for(m=0;m < 48 ;m++){ keys[ 2][m] = tempKey[m]; } break;  
     case 3: for(m=0;m < 48 ;m++){ keys[ 3][m] = tempKey[m]; } break;  
     case 4: for(m=0;m < 48 ;m++){ keys[ 4][m] = tempKey[m]; } break;  
     case 5: for(m=0;m < 48 ;m++){ keys[ 5][m] = tempKey[m]; } break;  
     case 6: for(m=0;m < 48 ;m++){ keys[ 6][m] = tempKey[m]; } break;  
     case 7: for(m=0;m < 48 ;m++){ keys[ 7][m] = tempKey[m]; } break;  
     case 8: for(m=0;m < 48 ;m++){ keys[ 8][m] = tempKey[m]; } break;  
     case 9: for(m=0;m < 48 ;m++){ keys[ 9][m] = tempKey[m]; } break;  
     case 10: for(m=0;m < 48 ;m++){ keys[10][m] = tempKey[m]; } break;  
     case 11: for(m=0;m < 48 ;m++){ keys[11][m] = tempKey[m]; } break;  
     case 12: for(m=0;m < 48 ;m++){ keys[12][m] = tempKey[m]; } break;  
     case 13: for(m=0;m < 48 ;m++){ keys[13][m] = tempKey[m]; } break;  
     case 14: for(m=0;m < 48 ;m++){ keys[14][m] = tempKey[m]; } break;  
     case 15: for(m=0;m < 48 ;m++){ keys[15][m] = tempKey[m]; } break;  
   }  
 }  
 return keys;    
}  
'''
