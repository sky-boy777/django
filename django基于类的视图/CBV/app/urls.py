"""CBV URL Configuration

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
                  # 类视图
   path('', views.IndexView.as_view(), name='index'),
   # TemplateView
   path('template/', views.TemplateView.as_view(), name='template'),
   # ListView
   path('list/', views.MyListView.as_view(), name='list'),
   # # CreateView
   # path('create/', views.MyCreateView.as_view(), name='create'),

]
