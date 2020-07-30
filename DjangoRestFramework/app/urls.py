"""DjangoRestFramework URL Configuration

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
from app import views

app_name = 'app'

urlpatterns = [
    # 查询所有
    path('info/', views.InfoView.as_view(), name='info'),
    # 查询一条，可以对应同一个类，只是定义的方法不同
    path('info/<int:did>/', views.InfoView.as_view(), name='info'),
    # 增（反序列化）,将数据存入数据库
    path('add/', views.AddView.as_view(), name='add'),
    # 接受json数据
    path('req/', views.RequestView.as_view(), name='req'),
    # fbv需要加装饰器
    path('fbv/', views.fbv, name='fbv'),
    # GenericAPIView
    path('data/<int:pk>/', views.UserInfoView.as_view(), name='data'),
    path('find/<int:pk>/', views.UserInfoFindView.as_view(), name='find'),
    # 设置身份验证
    path('token/', views.set_token, name='token'),
    # 分页
    path('page/', views.DataView.as_view(), name='page'),
    # 过滤
    path('list/', views.ListView.as_view(), name='list'),
]
