from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView # 导入views下的子类generic，类视图要继承generic
from app.models import Data  # 数据表
from django.utils.decorators import method_decorator  # 类视图使用装饰器要导入的类


# 路由保护装饰器
def check_login(fun):
    def inner(request, *args,  **kwargs):
        if 1:  # request.session.get('username'):  # 判断是否登录
            return fun(request, *args, **kwargs)  # 执行被装饰的函数
        else:
            return redirect('/')  # 跳转到首页
        return inner  # 返回内部函数


# 类视图的使用                    dispatch:全部装饰
# @method_decorator(check_login, name='dispatch')  # 类视图使用装饰器@method_decorator(装饰器名， name)
class IndexView(View):  # 函数对应的方法['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    '''什么样的请求对应什么样的方法'''
    def get(self, request):
        print(request.method)
        return HttpResponse('get')

    @method_decorator(check_login)  # 只装饰post方法
    def post(self, request):
        return HttpResponse('post')

    def put(self, request):
        return HttpResponse('put')

    def delete(self, request):
        return HttpResponse('delete')


class TemplateView(TemplateView):
    # 模板文件名
    template_name = 'template.html'
    # 获取模板中的数据
    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['name'] = '模板视图'
        return kwargs

class MyListView(ListView):
    '''要返回查询结果集objectset'''
    # # 模板文件名
    template_name = 'list.html'
    # 可以的属性
    # allow_empty = True
    # queryset = None
    # model = None
    # paginate_by = None
    # paginate_orphans = 0
    # context_object_name = None
    # paginator_class = Paginator
    # page_kwarg = 'page'
    # ordering = None

    paginate_by = 5  # 分页显示，每页显示5个
    ordering = ['-id']  # 按id降序排序,列表

    # 最后返回的查询结果集，名字必须时queryset
    queryset = Data.objects.all()

    # 重写get_queryset方法,如果排序也要写在里面
    # def get_queryset(self):
    #     data = Data.objects.all()
    #     return data


# class MyDetailView(DetailView):
#     template_name = 'detail.html'
#     queryset = Data.objects.all()
#     context_object_name = 'data'


# class MyCreateView(CreateView):
#     '''创建用户'''
#     template_name = 'create.html'
#     model = User
#     # 字段列表， 用于创建用户时设定用户属性
#     fields = ['username','password']
#     success_url = '/'  # 创建成功后跳转的地址

