===============================================
DutSSO
===============================================

DutSSO是一个可以使你快速登录大连理工大学统一身份认证系统并获取个人信息的一个Python模块，是本人在写网络爬虫的过程中总结出来的。由于服务器认证方式可能发生变化，所以请在无法使用时及时告知于我，我会及时做出更新。

本人邮箱：yuanyuanzijin@gmail.com

QQ群：344247954（DUT AI Lab），大连理工大学程序员聚集地，欢迎大家加入！



重要公告
==============

V0.10.5 邮件支持添加附件

V0.10.0 加入查询本科成绩的方法

V0.9.0 加入密文登录，以提高信息的安全性，如需储存账号密码，请使用密文方式。使用方法请参考examples文件夹中的 `encrypt_basic <https://github.com/yuanyuanzijin/dutsso/blob/master/examples/-2_encrypt_basic.py>`_ ！

V0.8.0 加入邮箱类，方便开发者发送邮件。


安装
================

环境：Python 3

在终端输入

::

    pip install git+https://github.com/yuanyuanzijin/dutsso

即可安装dutsso的最新版本。

由于这是一个新项目，且服务器认证方式可能发生变化，请在使用前检查最新版本，以获得更好的使用体验。


功能概述
==============

详细使用文档请查看 Document_ 。

.. _Document: https://github.com/yuanyuanzijin/DutSSO/wiki/Document

User类
--------------

* 初始化对象 u = dutsso.User()

* 用户登录 u.login()

* 获取密文密码 u.get_encrypted_password()

* 检测登录状态 u.isactive()

* 退出登录 u.logout()

* 获取个人信息 u.get_all_info()

* 获取校园卡信息 u.get_card()

* 获取图书借阅信息 u.get_library()

* 获取校园网使用信息 u.get_network()

* 获取校园邮箱信息 u.get_email()

* 获取浴室人数信息 u.get_bathroom()

* 获取研究生成绩 u.get_score_yjs()

* 获取研究生培养方案 u.get_plan_yjs()

* 研究生选课 u.choose_course_yjs()

* 研究生课程评价（可更新评价） u.evaluate_course_yjs()

* 获取大工就业网招聘信息 u.get_job()

* 获取本科成绩 u.get_score_bks()


Mail类
----------------

* 初始化对象 m = dutsso.Mail()

* 邮件发送 m.send()

以上只是部分方法，详细使用文档请查看 Document_ 。

.. _Document: https://github.com/yuanyuanzijin/DutSSO/wiki/Document


基本示例
==============

使用示例展示了各个功能的基本用法，可供新手参考。基本示例存放在 `Examples <https://github.com/yuanyuanzijin/dutsso/tree/master/examples>`_ 文件夹中。

需要登录的功能
--------------

* `基本使用（创建用户，登录，登出，查询登录状态） <https://github.com/yuanyuanzijin/dutsso/blob/master/examples/0_basic.py>`_

* `密文登录基本使用 <https://github.com/yuanyuanzijin/dutsso/blob/master/examples/-2_encrypt_basic.py>`_

* `获取用户信息 <https://github.com/yuanyuanzijin/dutsso/blob/master/examples/1_get_user_info.py>`_

* `获取玉兰卡信息 <https://github.com/yuanyuanzijin/dutsso/blob/master/examples/2_get_card.py>`_

* `获取校园网信息 <https://github.com/yuanyuanzijin/dutsso/blob/master/examples/3_get_network.py>`_

* `获取校园邮箱 <https://github.com/yuanyuanzijin/dutsso/blob/master/examples/4_get_email.py>`_

* `获取图书馆借书信息 <https://github.com/yuanyuanzijin/dutsso/blob/master/examples/5_get_library.py>`_

* `获取浴室实时人数信息 <https://github.com/yuanyuanzijin/dutsso/blob/master/examples/6_get_bathroom.py>`_

* `获取成绩（本科生） <https://github.com/yuanyuanzijin/dutsso/blob/master/examples/11_bks_get_score.py>`_

* `获取培养计划（研究生） <https://github.com/yuanyuanzijin/dutsso/blob/master/examples/21_yjs_get_plan.py>`_

* `获取成绩（研究生） <https://github.com/yuanyuanzijin/dutsso/blob/master/examples/22_yjs_get_score.py>`_

* `学生选课（研究生） <https://github.com/yuanyuanzijin/dutsso/blob/master/examples/23_yjs_choose_course.py>`_

* `课程评价（研究生） <https://github.com/yuanyuanzijin/dutsso/blob/master/examples/24_yjs_evaluate_course.py>`_

不需要登录的功能
----------------

* `邮件基本使用 <https://github.com/yuanyuanzijin/dutsso/blob/master/examples/-1_mail_basic.py>`_

* `获取大工就业网招聘信息 <https://github.com/yuanyuanzijin/dutsso/blob/master/examples/8_get_jobs.py>`_


进阶项目
================

进阶项目包括了基于dutsso的复杂项目，可以理解为将examples中的示例运用到了实际项目中。

- 多用户管理系统

管理多个用户账号和密码的脚本程序，信息存在sqlite数据库中，以供其他项目使用，密码转化为密文储存。详见 `multi_users_admin <https://github.com/yuanyuanzijin/dutsso/tree/master/projects/multi_users_admin>`_ 。

- 研究生新成绩提醒

查询研究生成绩，和数据库中的比对，发现新成绩后自动发送邮件提醒。配合操作系统的定时运行，可实现自动提醒新成绩。详见 `yjs_score_send_email <https://github.com/yuanyuanzijin/dutsso/tree/master/projects/yjs_score_send_email>`_ 。

- 浴室人数实时监控

从配置文件中获取用户名和密文密码，自动登录查询浴室人数，并保存到sqlite3数据库中。配合操作系统的定时执行，可实现自动监控。详见 `save_bathroom_info <https://github.com/yuanyuanzijin/dutsso/tree/master/projects/save_bathroom_info>`_ 。

- 大工就业网招聘信息自动发送程序

查询大工就业网指定日期的招聘信息，发送给mail_list中的邮箱。配合操作系统的定时执行，可实现每天定时发送。详见 `get_jobs_and_send_email <https://github.com/yuanyuanzijin/dutsso/tree/master/projects/get_jobs_and_send_email>`_ 。


更多基于或参考DutSSO的项目
===========

- Score_Send_Email

定时查询成绩，获取到新成绩后，发送邮件提醒，程序一直运行，未使用操作系统的定时任务，不适合长期执行。详见本人项目 `Zijinlib/projects/score_send_email/`_ 。

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