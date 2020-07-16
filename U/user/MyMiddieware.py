from django.shortcuts import HttpResponse, redirect, reverse
from django.utils.deprecation import MiddlewareMixin  # 自定义中间件要继承的父类


# 可实现：统计、黑名单、白名单、界面友好话（只有本地登录才能看到异常）
class MyMiddieware(MiddlewareMixin):
# 1(执行顺序)
     # 在每个请求前调用
     def process_request(self, request):
         print('请求调用前')
         return None


# 3
     # 每个响应返回浏览器之前调用()
     def process_response(self, request, response):
         print('响应返回前调用')
         return response  # 必须返回response（跟scrapy基本一样）


# 2
     # 到视图的时候执行
     def process_view(self, request, vies_func, view_args, view_kwargs):
         print('执行视图函数前调用')


     # 视图抛出异常时执行，返回None或HttpResponse对象
     def process_exception(self, request, response):
        print('出错的时候执行')

        # 如何ip为本机地址，则显示错误的信息，否则重定向到主页
        ip = request.META.get('REMOTE_ADDR')
        if ip == '127.0.0.1':
            return
        else:
            return redirect(reverse('user:index'))