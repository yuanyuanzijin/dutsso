# 浴室人数监控程序

## 功能简介
该程序可在每天的13:00到22:00每5分钟保存一次浴室信息到sqlite3数据库中，以供日后分析。

## 使用方法

1. 安装最新版dutsso（如python默认版本为python2，请使用pip3）：

```
pip install git+https://github.com/yuanyuanzijin/dutsso
```

2. git clone本项目的最新版：

```
git clone https://github.com/yuanyuanzijin/dutsso
```

3. 将projects文件夹下的save_bathroom_info文件夹拷贝到自己的项目路径下，并删除index.py文件中的前两行。

4. 获取自己的密文密码，可在clone下来的dutsso目录下执行获得：

```
python3 examples/-2_encrypt_basic.py
```

5. 将single_user_config.ini.example修改为自己的用户名和密文密码，并重命名为single_user_config.ini。

6. 将bathroom.db.example重命名为bathroom.db。

截止到目前，您的项目已经可以运行了。sqlite3数据库可用数据库查看软件进行查看。

以下是定时运行的方法(Ubuntu)——

7. 修改bathroom.cron为：

```
*/5 12-22 * * * python3 <项目路径>/index.py > /dev/null 2>&1
```

*/5代表每5分钟执行一次，12-22代表每天的12点到22点执行，中间的指令要保证能运行（可提前在终端测试通过，报错要及时改正），>后面的不明白可以直接copy

8. 开启定时任务：

```
crontab <项目路径>/bathroom.cron > log
```