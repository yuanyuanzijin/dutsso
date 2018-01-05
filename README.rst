===============================================
python-dutsso
===============================================

Dutsso是一个可以使你登录大连理工大学统一身份认证系统的一个python包，是本人在写网络爬虫的过程中总结出来的。由于服务器认证方式可能发生变化，所以请在无法使用时及时告知于我，我会及时做出更新。

本人邮箱：yuanyuanzijin@gmail.com。

安装
================

在终端输入

``pip install git+https://github.com/yuanyuanzijin/python-dutsso`` 

即可安装dutsso的最新版本。

由于这是一个新项目，且服务器认证方式可能发生变化，请在使用前检查最新版本，以获得更好的使用体验，

使用
===========

请在程序的开头使用``import dutsso``来引入dutsso。

衍生项目
===========

- Score_Send_Email

定时查询成绩，获取到新成绩后，发送邮件提醒。详见本人项目 `Python-Zijinlib/projects/score_send_email/`_ 。

.. _`Python-Zijinlib/projects/score_send_email/`: https://github.com/yuanyuanzijin/python-zijinlib/tree/master/projects/score_send_email

- Score_yzm

大连理工大学研究生成绩查询，未使用SSO，需要验证码。详见本人项目 `Web-Crawler/score/`_ 。

.. _`Web-Crawler/score/`: https://github.com/yuanyuanzijin/web-crawler/blob/master/score

- Score-Crawler

东北大学研究生成绩查询，可跳过验证码。详见Onionwyl的项目 `Score-Crawler`_ 。

.. _`Score-Crawler`: https://github.com/onionwyl/score-crawler


文档
=============

User.__init__(self, username='', password='')
-------------

User对象初始化方法，在创建对象时自动调用，可传入用户名和密码（或稍后设置）。

示例：

::

    u = dutsso.User()

    u.username = "123456"

    u.password = "000000"

    或

    u = dutsso.User("123456", "000000")


User.login(self, try_cookies=True, auto_save=True)
-------------

用户登录的方法。请在使用其他方法前调用此方法，以取得登录状态。

try_cookies参数代表是否尝试从cookies文件中恢复登录状态，默认为True。

auto_save参数代表是否在登录成功后保存cookies信息到文件中，以方便下次登录，默认为True。

返回布尔值，True代表登录成功，False代表登录失败。

示例：

::

    back = u.login(try_cookies=True, auto_save=True)


User.get_card(self)
-------------

获取校园卡信息的方法。

返回Json格式的校园卡信息。

示例：

::

    card = u.get_card()


User.get_score(self)
-------------

获取研究生成绩的方法。

返回Json格式的成绩信息。

示例：

::

    scores = u.get_score()


User.get_library(self)
------------

获取图书馆借书信息的方法。

返回Json格式的借书信息。

示例：

::

    lib_list = u.get_library()


User.logout(self, clear_save=False, path="./")
--------------

退出登录的方法，可清除当前cookies。clear_save参数为是否清除保存cookies的文件，默认为False。

User.cookies_get(self)
--------------

手动获取当前cookies的方法。

User.cookies_save(self, cookies_dict=None, path="./")
---------------

手动保存当前cookies字典到文件中的方法。

User.cookies_set(self, cookies_dict)
--------------

手动从字典中设置新cookies的方法。

User.cookies_restore(self, path='./')
--------------

手动从文件中恢复cookies值给当前用户的方法。

其他
==============

文档持续更新中，使用方式请参考 Example.py_ 。


.. _Example.py: https://github.com/yuanyuanzijin/python-dutsso/blob/master/example.py

