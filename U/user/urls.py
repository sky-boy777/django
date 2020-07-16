"""U URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # 路由保护(登录后才能访问)
    path('a/', views.a, name='a'),
    # 修改密码
    path('change_password', views.change_password, name='change_password'),

    # 发送邮件
    path('send/', views.mail_send, name='name'),
    # 富文本框编辑器
    path('edit/', views.my_edit, name='edit'),
    # 文件上传
    path('file/', views.file, name='file'),
    # 手动设置缓存
    path('cache/', views.my_cache, name='cache'),
    # 邮箱激活账号，要接受token参数
    path('active/<token>/', views.emial_active, name='active'),
]
