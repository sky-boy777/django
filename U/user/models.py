from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.数据库模型：类==表，对象==一行，属性==字段
class User(AbstractUser):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=30, verbose_name='用户名')
    password = models.CharField(max_length=254)
    is_active = models.SmallIntegerField(default=1, verbose_name='激活状态')  # 是否激活，1为激活，0为未激活

    class Meta:
        db_table = 'user'



class Data(models.Model):
    text = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'data'
