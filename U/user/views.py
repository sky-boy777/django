from django.shortcuts import render, HttpResponse, redirect, reverse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout   # 查数据库验证， 登录， 退出登录
from django.contrib.auth.decorators import login_required  # 路由保护装饰器
from user.models import User, Data # 用户表
from user.forms import Form  # 表单验证类（自定义的）
from django.core.mail import send_mail, send_mass_mail  # 发送一封或多封邮件
from U.settings import STATICFILSE_DIRS
import os
import datetime
import random
from django.views.decorators.cache import cache_page  # 页面缓存

from django.template import loader  # 渲染成HTML形式发送邮件

# 生成token两种方法
# 方法一
# from user.util import token_confirm   # 导入自定义生成token的Py文件

# 方法二
from itsdangerous import TimedJSONWebSignatureSerializer  # 生成token
from itsdangerous import SignatureExpired  # token超时发生的异常

# celery
from celery_tasks.tasks import send_register_active_emial

def register(request):
    if request.method == 'POST':
        form = Form(request.POST)
        # 验证
        if form.is_valid:
            data = request.POST.dict()
            username = data.get('username')
            password = data.get('password')

            # 写入数据库，create_user会做密码签名（加密）
            try:
                user = User.objects.create_user(username=username, password=password)
                # is_active设置为0,表示未激活，后面需要邮箱验证激活
                user.is_active = 0
                user.save()
            except:
                # 插入数据库失败的其他原因
                return render(request, 'register.html', {'content': '用户名已存在'})

# 邮箱验证激活账号开始
            # 如果数据库里有用户，则发送邮件激活账号
            if user:
                # 方法一，使用自定义封装的类生成加密token
                # token = token_confirm.generate_validate_token(user.uid)

                # 方法二，直接使用第三方生成加密token                          超时时间（秒）
                serializer = TimedJSONWebSignatureSerializer('SECRET_KEY', 3600)
                info = {'uid': user.uid}  # 要加密的字典
                token = serializer.dumps(info)   # 加密，生成token
                token = token.decode('utf-8')  #  生成的token默认是byte类型，需要解码

                #                  服务器地址          路由     参数
                # 构造激活url： http://127.0.0.1:8000/active/dkfjiaflsdfjdkfja   (token密钥)
                # url = 'http://' + request.get_host() + reverse('user:active', kwargs={'token': token})

                # 渲染html模板： 导入from django.template import loader
                # 方法一
                # html = loader.get_template('active.html').render({'url': url})

                # 方法二，HTML模板
                html = '<h1>%s,欢迎你注册</h1> 点击下面链接激活账号<br> <a href="http://127.0.0.1:8000/active/%s">http://127.0.0.1:8000/active/%s</a">' % (username, token, token)
                # 发送邮件
                send_mail('账号激活', '', '1251779123@qq.com', [request.POST.get('emial')], html_message=html)

                # 方法三，使用celery发送邮件(任务发出者)，发送到任务队列（中间人redis），任务处理者监听队列
                # send_register_active_emial.delay(request.POST.get('emial'), username, token)

                return HttpResponse('邮件已发送，请登录邮箱点击激活账号')
# 结束

            else:
                # 用户名已存在的情况
                return render(request, 'register.html', {'content': '用户名已存在'})

    return render(request, 'register.html')


# 登录，不要用login，会跟用户验证中的login冲突
def user_login(request):
    if request.method == 'POST':
        form = Form(request.POST)
        # 验证
        if form.is_valid:
            data = request.POST.dict()
            username = data.get('username')
            password = data.get('password')

            # 用户验证，如果用户名和密码正确，返回user对象，否则返回None
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)  # 记住用户登录状态,将user赋值给request
                # return redirect('/')  # 重定向
                # return redirect('user:index')  # 重定向
                return redirect(reverse('user:index'))  # 重定向
                # return HttpResponseRedirect('/')  # 重定向
                # return HttpResponseRedirect(reverse('user:index'))  # 重定向 user:index
            else:
                return render(request, 'login.html', {'content': '用户名或密码错误,只有激活的账号才能登录'})
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect(reverse('user:index'))

# 缓存装饰器，后面为时间（秒）
@cache_page(1)
def index(request):                               # 格式时间
    my_time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    my_time2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 判断是否登录
    if authenticate(request):
        return render(request, 'index.html')
    else:
        return render(request, 'index.html', locals())


                # 未登录，跳转下面的路由
@login_required(login_url='user:login')
# @login_required(login_url='/login/')
def a(request):
    return HttpResponse('<h1>后台<h1>')


# 修改密码
@login_required(login_url='user:login')
def change_password(request):
    # print(request.user.username)
    if request.method == 'POST':
        # 用户验证，如果当前登录的用户名和表单输入的旧密码密码正确，则返回user对象，否则返回None
        user = authenticate(request, username=request.user.username, password=request.POST.get('old_password'))
        if user:
            try:
                if len(request.POST.get('new_password')) < 3:  # 判断新密码是否符合规则
                    return render(request, 'change_password.html', {'content': '密码长度不能小于3位'})

                user = User.objects.get(username=request.user.username)  # 获取得用户实例对象
                user.set_password(request.POST.get('new_password'))   # 修改密码
                user.save()   # 保存
            except:
                return render(request, 'change_password.html', {'content': '出错了'})

            # 无错误，则先退出登录状态，然后去到登录页面重新登录
            logout(request)
            return redirect('user:login')
        else:
            return render(request, 'change_password.html', {'content': '旧密码输入错误'})

    # GET方法
    return render(request, 'change_password.html')


# 发送邮件
def mail_send(request):
    # 发送一封邮件
    # send_mail(主题，   内容，    从哪发送(发送人账号)，      接受人列表,       ...)  前四个必填
    # send_mail('邮箱主题', '这是内容<a href="http://127.0.0.1:8000/">返回</a>', '1251779123@qq.com', ['1251779123@qq.com'])

    # 发送多封邮件
    m1 = ('邮箱主题', '1', '1251779123@qq.com', ['1251779123@qq.com'])
    m2 = ('邮箱主题', '2', '1251779123@qq.com', ['1251779123@qq.com'])
    m3 = ('邮箱主题', '3', '1251779123@qq.com', ['1251779123@qq.com'])
    m4 = ('邮箱主题', '4', '1251779123@qq.com', ['1251779123@qq.com'])
    send_mass_mail((m1, m2, m3, m4))

    return HttpResponse('发送成功')


# 富文本框
def my_edit(request):
    if request.method == 'POST':
        print(request.POST.get('content'))
    return render(request, 'edit.html')

# 文件上传
def file(request):
    if request.method == 'POST':
        # 获取文件对象
        fobj = request.FILES.get('photo')
        # 如果有文件，并且文件小于30M，则保存文件
        if fobj and fobj.size < 1024*1024*30:
            # 创建文件路径（放在static/file/文件名）
            path = os.path.join(STATICFILSE_DIRS[0], 'file/')
            # 创建文件名：当前时间 + 一个随机数 + ‘-’ + 上传的文件名
            file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(1, 10000)) + '-' + fobj.name
            # 合并得到最终的文件名路径
            path = os.path.join(path, file_name)
            # 保存文件
            with open(path, 'wb')as f:
                # 判断文件是否大于2.5m，大于则按块写入，否则直接写入
                if fobj.multiple_chunks():
                    for data in fobj.chunks():
                        f.write(data)
                else:
                    f.write(fobj.read())
                return render(request, 'file.html', {'content': '上传成功'})
        else:
            return render(request, 'file.html', {'content': '这文件不对头'})
    return render(request, 'file.html')


# 手动设置缓存
def my_cache(request):
    from django.core.cache import cache  # 手动设置缓存，导入底层的缓存
    # 首先在缓存表里查数据
    my_data = cache.get('all_data')
    # 缓存表里没有再到数据库里查并将数据放入缓存表里
    if not my_data:
        my_data = Data.objects.all()
        # cache可以直接把查询结果序列化,保存到缓存表里
        cache.set('all_data', my_data, 20)  # cache.set(key, value, timeout(秒))
    return render(request, 'cache.html', locals())


# 邮箱验证激活账号
def emial_active(request, token):
    try:
        # uid = token_confirm.confirm_validte_token(token)   # 方法一，解密token，将uid取出来

        serializer = TimedJSONWebSignatureSerializer('SECRET_KEY', 3600)  # 方法二
        info = serializer.loads(token)  # 解密，加密的时候是字典，解密的时候还是字典
        uid = info.get('uid')
    except SignatureExpired as e:   # token过期的错误SignatureExpired
        # uid = token_confirm.remove_validate_token(token)  # 方法一，解密出错则删除token

        user = User.objects.get(pk=uid)  # 连账号也删除，让用户重新注册
        user.delete()
        return HttpResponse('激活链接过期，请重新注册')
    try:
        user = User.objects.get(pk=uid)  # 在数据库里查找用户，找不到则表示用户不存在
    except:
        return HttpResponse('用户不存在，请重新注册')

    # 激活
    user.is_active = 1
    user.save()
    return redirect(reverse('user:login'))  # 激活成功，重定向到登录页面