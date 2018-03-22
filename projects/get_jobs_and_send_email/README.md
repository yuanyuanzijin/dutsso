# 招聘信息定时发送程序

## 功能简介

该程序可以每日定时自动发送最新的大工就业网招聘信息到指定邮箱中。

## 使用方法

1. 安装最新版dutsso（如python默认版本为python2，请使用pip3）：

```
pip install git+https://github.com/yuanyuanzijin/dutsso
```

2. git clone本项目的最新版：

```
git clone https://github.com/yuanyuanzijin/dutsso
```

3. 将projects文件夹下的get_jobs_and_send_email文件夹拷贝到自己的项目路径下，并删除index.py文件中的前两行。

4. 将mail_list.txt.example修改为自己的邮箱，并重命名为mail_list.txt。

5. 配置dutsso文件夹下的mail_config.ini.example为自己的配置，并重命名为mail_config.ini，放在本项目文件夹中，并修改index.py中mail_config.ini的路径。

截止到目前，您的项目已经可以运行了。sqlite3数据库可用数据库查看软件进行查看。

以下是定时运行的方法(Ubuntu)——

5. 修改jobs.cron为：

```
0 8 * * * python3 <项目路径>/index.py > /dev/null 2>&1
```

0代表0分执行，8代表每天的8点执行，中间的指令要保证能运行（可提前在终端测试通过，报错要及时改正），>后面的不明白可以直接copy

6. 开启定时任务：

```
crontab <项目路径>/jobs.cron > log
```