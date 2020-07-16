# 使用celery
from celery import Celery
from django.core.mail import send_mail  # 发送邮件
from U.settings import EMAIL_FROM  # 服务器发送邮件的邮箱
import time


# 如果任务处理者（worker）在另一台电脑启动则需要把整个项目代码复制一份过去，而且要在worker加上下面四句，为了加载配置
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'U.settings')
# import django
# django.setup()


# 创建Celery类实例对象
# main一般为tasks的路径                   中间人redis地址，使用6号数据库
app = Celery(main='celery_tasks_tasks', broker='redis://127.0.0.1/6')


# 定义任务函数，发送注册激活邮件
@app.task
def send_register_active_emial(to_emial, username, token):
    '''发送激活邮件
    to_emial: 发给谁
    username: 用户名
    token: token值
    '''
    # 组织邮件信息
    html = '<h1>%s,欢迎你注册</h1> 点击下面链接激活账号<br> <a href="http://127.0.0.1:8000/active/%s">http://127.0.0.1:8000/active/%s</a">' % (
    username, token, token)

    # 发送邮件
    send_mail('账号激活', '', EMAIL_FROM, [to_emial], html_message=html)
    time.sleep(5)
