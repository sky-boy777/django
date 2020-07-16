from django.contrib import admin
from .models import User, Data  # 导入模型

# Register your models here.

# 配置后台页面和添加数据的展示
class UserAdmin(admin.ModelAdmin):
    # 可以显示的字段
    list_display = ['pk', 'username', 'is_active', 'password']
    # 搜所字段
    search_fields = ['username']
    # 过滤
    list_filter = ['username']
    # 信息分组
    fieldsets = [
        ('用户名信息', {'fields': ['username']}),
        ('密码', {'fields': ['password']}),
    ]


class DataAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']
    list_per_page = 10  # 每页显示10条


# 注册（在后台显示表，然后可以修改表数据）
admin.site.register(User, UserAdmin)
admin.site.register(Data, DataAdmin)