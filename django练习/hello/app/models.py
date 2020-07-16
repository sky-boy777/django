from django.db import models

# Create your models here.数据库模型：类==表，对象==一行，属性==字段
class User(models.Model):
    uid = models.AutoField(primary_key=True)  # 主键、指定字段名
    username = models.CharField(max_length=16)  
    password = models.CharField(max_length=128)

    class Meta: 
        # 默认：应用名_模型名（App_User）
        db_table = 'user'  # 指定表名


