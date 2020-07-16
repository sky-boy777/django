"""hello URL Configuration
hello URL Configuration

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
from app import views 
from django.urls import path

app_name = 'app'  # 应用命名空间

urlpatterns = [
	# 主页
    path('', views.index, name='index'),

    # 登录
    path('login/', views.login, name='login'),

    # 退出登录
    path('logout/', views.logout, name='logout'),

   # 注册
    path('register/', views.register, name='register'),

    # 只有登录后才能访问的页面（路由保护）
    path('user/', views.user, name='user'),

    # 验证码
    path('cap/', views.cap, name='cap'),

]
