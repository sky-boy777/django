from rest_framework.pagination import PageNumberPagination, OrderedDict
from rest_framework.response import Response

# 自定义分页类
class MyPage(PageNumberPagination):
    page_size = 5  # 每页数目，为空则表示禁用分页
    page_size_query_param = 'page_size'  # 页面大小，可以由前端传过来

    # 自定义分页形式, 重写get_paginated_response方法
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),  # 总数
            ('page_range', list(self.page.paginator.page_range)),  # 页码范围
            ('has_next', self.page.has_next()),   # 是否有下一页
            ('has_prious', self.page.has_previous()),  # 是否有上一页
            ('next_page_number', self.page.next_page_number()),  # 下一页页码
            ('results', data)  #
        ]))