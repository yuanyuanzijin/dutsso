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
=============

请在程序的开头使用``import dutsso``来引入dutsso。

文档
=============

User类
-------------

* User.login(self, username, password)

用户登录的方法。请在使用其他方法前调用此方法，已取得登录状态。
返回布尔值，True代表登录成功，False代表登录失败。

示例：
u = dutsso.User()
back = u.login(username, password)

* User.get_card(self)

获取校园卡信息的方法。
返回Json格式的校园卡信息。

示例：
card = u.get_card()

* User.get_score(self)

获取研究生成绩的方法。
返回Json格式的成绩信息。

示例：
score = u.get_score()

* User.get_library(self)

获取图书馆借书信息的方法。
返回Json格式的借书信息。

示例：
score = u.get_library()

文档持续更新中，请参考example.py。

