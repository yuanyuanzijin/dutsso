===============================================
DutSSO
===============================================

DutSSO是一个可以使你快速登录大连理工大学统一身份认证系统并获取个人信息的一个Python模块，是本人在写网络爬虫的过程中总结出来的。由于服务器认证方式可能发生变化，所以请在无法使用时及时告知于我，我会及时做出更新。

本人邮箱：yuanyuanzijin@gmail.com。
QQ群：344247954（DUT AI Lab），大连理工大学程序员聚集地，欢迎大家加入！


基于或参考DutSSO的项目
===========

- Score_Send_Email

定时查询成绩，获取到新成绩后，发送邮件提醒。详见本人项目 `Zijinlib/projects/score_send_email/`_ 。

.. _`Zijinlib/projects/score_send_email/`: https://github.com/yuanyuanzijin/zijinlib/tree/master/projects/score_send_email

- Choose_Course

大连理工大学研究生选课脚本，定时查询课余量并选课。详见本人项目 `Zijinlib/projects/choose_course`_ 。

.. _`Zijinlib/projects/choose_course`: https://github.com/yuanyuanzijin/zijinlib/tree/master/projects/choose_course

- Score_yzm

大连理工大学研究生成绩查询，未使用SSO，需要验证码。详见本人项目 `Web-Crawler/score/`_ 。

.. _`Web-Crawler/score/`: https://github.com/yuanyuanzijin/web-crawler/blob/master/score

- Score-Crawler

东北大学研究生成绩查询，可跳过验证码。详见Onionwyl的项目 `Score-Crawler`_ 。

.. _`Score-Crawler`: https://github.com/onionwyl/score-crawler


安装
================

环境：Python 3

在终端输入

::

    pip install git+https://github.com/yuanyuanzijin/dutsso

即可安装dutsso的最新版本。

由于这是一个新项目，且服务器认证方式可能发生变化，请在使用前检查最新版本，以获得更好的使用体验，

功能概述
==============

详细使用文档请查看 Document_ 。

.. _Document: https://github.com/yuanyuanzijin/DutSSO/wiki/Document

* 用户登录 User.login()

* 检测登录状态 User.isactive()

* 退出登录 User.logout()

* 获取个人信息 User.get_all_info()

* 获取校园卡信息 User.get_card()

* 获取图书借阅信息 User.get_library()

* 获取校园网使用信息 User.get_network()

* 获取校园邮箱信息 User.get_email()

* 获取研究生成绩 User.get_score_yjs()

* 获取研究生培养方案 User.get_plan_yjs()

* 研究生选课 User.choose_course_yjs()

* 研究生课程评价（可修改评价） User.evaluate_course_yjs()

以上只是部分方法，详细使用文档请查看 Document_ 。

.. _Document: https://github.com/yuanyuanzijin/DutSSO/wiki/Document


其他
==============

使用示例请参考 Example.py_ 。


.. _Example.py: https://github.com/yuanyuanzijin/python-dutsso/blob/master/example.py

