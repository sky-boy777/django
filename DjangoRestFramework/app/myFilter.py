from django_filters import rest_framework as filters
from app.models import Data

# 自定义过滤类
class MyFilter(filters.FilterSet):
    class Meta:
        model = Data  # 指定模型

        # 字段过滤
        fields = {
            # 跟ORM运算一样
            # http://127.0.0.1:8000/list/?id__gt=5, 过滤id大于5的
            'id': ['exact', 'lt', 'lte', 'in'],  # 等于，小于,小于等于，在里面
            'text': ['icontains', 'startswith', 'iendswith'],  # 包含、以什么开头，以什么结尾
        }



