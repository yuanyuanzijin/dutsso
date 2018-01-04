import requests
from bs4 import BeautifulSoup
import execjs

class User:
    def __init__(self):
        self.s = requests.Session()
    
    def __get_key(self, username, password, ticket):  
        f = open("./des.js", 'r', encoding='UTF-8')  
        line = f.readline()  
        htmlstr = ''  
        while line:  
            htmlstr = htmlstr + line  
            line = f.readline()
        ctx = execjs.compile(htmlstr)
        rsa = ctx.call('strEnc',username+password+ticket, '1', '2', '3')
        return rsa
    
    def login(self, username, password):
        self.username = username
        self.password = password

        url = "https://sso.dlut.edu.cn/cas/login?service=http://portal.dlut.edu.cn/tp/"
        req = self.s.get(url, allow_redirects=False)
        soup = BeautifulSoup(req.text, 'html.parser')

        ticket = soup.select('#lt')[0]['value']
        execution = soup.select('input')[4]['value']
        rsa = self.__get_key(username, password, ticket)
        jsessionid = req.cookies['JSESSIONID']

        url2 = "https://sso.dlut.edu.cn/cas/login;jsessionid=%s?service=http://portal.dlut.edu.cn/tp/" % jsessionid

        data = {
            'rsa': rsa,
            'ul': len(username),
            'pl': len(password),
            'lt': ticket,
            'execution': execution,
            '_eventId': 'submit'
        }

        req = self.s.post(url2, data=data, allow_redirects=False)
        soup = BeautifulSoup(req.text, 'html.parser')
        newaddr = soup.select('a')[0]['href']
        if newaddr.find("javascript") < 0:
            return True
        else:
            return False

    def get_card(self):
        url_card = "http://202.118.64.15/fabu/sso_jump.jsp"
        req = self.s.get(url_card)
        soup = BeautifulSoup(req.text, 'html.parser')
        money = soup.select('#information td')[5].text.strip().strip("元")
        last_time = soup.select('#information td')[7].text.strip()
        info = {
            "money": money,
            "last_time": last_time
        }
        return info

    def get_score(self):
        req = self.s.get("https://sso.dlut.edu.cn/cas/login?service=http://202.118.65.123/gmis/LoginCAS.aspx")
        req = self.s.get('http://202.118.65.123/pyxx/grgl/xskccjcx.aspx?xh=%s' % self.username)
        soup = BeautifulSoup(req.text, 'html.parser')

        bx_scores = soup.select('#MainWork_dgData tr')[1:]
        bx_dict = {}
        for score in bx_scores:
            soup1 = BeautifulSoup(str(score), 'html.parser')
            name = soup1.select('td')[0].text
            value = soup1.select('span')[0].text
            bx_dict[name] = value
        
        xx_dict = {}
        xx_scores = soup.select('#MainWork_Datagrid1 tr')[1:]
        for score in xx_scores:
            soup2 = BeautifulSoup(str(score), 'html.parser')
            name = soup2.select('td')[0].text
            value = soup2.select('span')[0].text
            xx_dict[name] = value
        
        scores = {
            "bx": bx_dict,
            "xx": xx_dict
        }
        return scores

    def get_library(self):
        url_card = "http://portal.dlut.edu.cn/sso/sso_tsg.jsp"
        req = self.s.get(url_card)
        soup = BeautifulSoup(req.text, "html.parser")
        time = soup.select('form input')[1]['value']
        verify = soup.select('form input')[2]['value']
        
        url_lib_login = "http://opac.lib.dlut.edu.cn/reader/hwthau.php"
        data = {
            'un': self.username,
            'time': time,
            'verify': verify
        }
        req = self.s.post(url_lib_login, data=data, allow_redirects=False)
        
        url_lib_info = "http://opac.lib.dlut.edu.cn/reader/redr_info_rule.php"
        req = self.s.get(url_lib_info)
        soup = BeautifulSoup(req.content.decode('utf-8'), 'html.parser')
        myinfo = soup.select('#mylib_content table tr')
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






