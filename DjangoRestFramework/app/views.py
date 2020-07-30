from django.shortcuts import render  # 快捷方式
from django.http import HttpResponse, JsonResponse  # 不是快捷方式
from rest_framework.generics import GenericAPIView, ListAPIView  # APIView子类，类视图要继承的父类
from rest_framework.views import APIView  # 也可见继承这个类，功能比GenericAPIView 少
from app.models import Data  # 数据表模型
from app.serializers import QbSerializers  # 自定义的序列号类
from rest_framework.response import Response  # 响应
from rest_framework.parsers import JSONParser  # 指定解析
from app.myAuthentications import MyAuthentications  # 认证
from app.myPerssions import MyPerssion  # 权限检查
from app.myThrottle import MyThrottle  # 节流
from rest_framework.pagination import PageNumberPagination  # 分页类
from app.myPagination import MyPage  # 自定义的分页类
from app.myFilter import MyFilter  # 自定义过滤


# 前后端分离
# Create your views here.
# 从数据库查询，转换成json数据传递给前端（序列化）
class InfoView(GenericAPIView):
    '''这是类视图1接口文档说明'''
    # 要有查询集
    queryset = Data.objects.all()

    # 处理get请求
    def get(self, request, did=0):
        # 查询所有段子信息
        # duanzi = Data.objects.all()

        # 序列化：将对象或queryset直接转换成字典或列表套字典
        # ds = QbSerializers(instance=self.queryset.all(), many=True)  # 多个对象则:many=True

        # 返回
        # return Response(ds.data)  # 返回，前端会收到json数据

        # 判断查询全部还是一条数据
        if did < 1:
            return self.find_all(request, did)
        return self.find_one(request, did)

    # 查询所有
    def find_all(self, request, did=0):
        ds = QbSerializers(instance=self.queryset.all(), many=True)  # 多个对象则:many=True
        return Response({
            'code': 200,
            'msg': 'ok',
            'data': ds.data,
        })  # 标准格式返回，前端会收到json数据

    # 查询一条
    def find_one(self, request, did):
        # 查询一个
        duanzi = self.queryset.get(id=did)
        # 序列化
        ds = QbSerializers(instance=duanzi)
        # 以json格式返回给前端
        return Response(ds.data)

# 接受前端传过来的json数据，转换成对象存入数据库（反序列化）
class AddView(GenericAPIView):
    '''这是类视图1接口文档说明'''
    queryset = Data.objects.all()
    serializer_class = QbSerializers

    def post(self, request):
        # 将前端传过来的数据反序列化，json字符串转换成对象
        ds = QbSerializers(data=request.data)
        # 验证数据
        if ds.is_valid():
            # 验证通过，保存到数据库
            ds.save()  # 调用的时create，直接创建并保存，如果是自定义的序列化器的话需要实现updata跟create方法
            return Response({"code": 1, 'msg': 'ok'})
        else:
            # 每通过，返回错误信息
            return Response({'code': 0,'msg': ds.errors})


class RequestView(APIView):
    '''这是类视图1接口文档说明'''
    # 自己指定解析器,是一个元组，可以多个
    parser_classes = (JSONParser,)  # 只解析jsop数据

    def get(self, request):
        print(request.data)   # request.data可以自动解析请求的数据，前端传过来的数据都在做了取
        print(request.query_params)  # 相当于request.GET,问号传参,get请求

        # Response可以将内置类型转换为字符串
        # data:内置类型数据：字典、列表、元组。不能是复杂对象。状态码。模板名。头部信息。内容类型
        # 响应对象传参Response(data=None, status=None,template_name=None, headers=None,content_type=None)
        return Response({'msg': 'ok'})
        # return Response([1, 2, 3])
        # return Response('hello')
        # return Response((3,5))


from rest_framework.decorators import api_view  # 用于基于函数的视图的装饰器

@api_view(['GET', 'POST'])  # 里面是请求方法，默认get
def fbv(request):
    '''这是普通视图1接口文档说明'''
    return Response('ok')


class UserInfoView(GenericAPIView):
    '''查询一个'''
    # 查询结果集（必须）
    queryset = Data.objects.all()
    # 序列化器（必须）
    serializer_class = QbSerializers


    # 认证
    authentication_classes = (MyAuthentications,)
    # 权限判断
    permission_classes = (MyPerssion,)
    # 节流（请求次数限制）
    throttle_classes = (MyThrottle,)



    def get(self, request, pk):
        # if request.query_params.get('token') != 'abcd':
        #     return Response({'msg': 0})
        obj = self.get_object()  # 获取一个对象，条件为pk
        da = QbSerializers(instance=obj)   # 序列化,多条数据需要加:many=True
        return Response(da.data)  # 返回为json数据


class UserInfoFindView(GenericAPIView):
    '''查询多的'''
    queryset = Data.objects.all()
    serializer_class = QbSerializers


    def get(self, request, pk):
        obj_set = self.get_queryset()  # 获取一个对象或查询及
        obj = obj_set.filter(pk=pk)  # 过滤条件
        da = QbSerializers(instance=obj, many=True)  # 序列化
        return Response(da.data)

# 模拟获取token
def set_token(request):
    return JsonResponse({'token': 'abcd'})



# 分页
class DataView(GenericAPIView):  # 继承ListAPIView可以快速实现分页
    queryset = Data.objects.all()  # 查询集（必须）
    serializer_class = QbSerializers  # 序列化器（必须）

    # 局部分页
    # pagination_class = PageNumberPagination  # 分页类
    # PageNumberPagination.page_size_query_param = 'page_size'  # 使用内置分页类必须声明这个，不声明默认禁用分页(None)
    pagination_class = MyPage  # 使用自定义的分页类

    # 继承GenericAPIView,如果继承ListAPIView则不用写下面
    def get(self, *args, **kwargs):
        # 过滤结果集
        queryset = self.filter_queryset(self.get_queryset())
        # 获取分页对象
        page = self.paginate_queryset(queryset=queryset)
        if page is not None:  # 分页对象存在
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # 不分页，返回所有数据
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# 过滤
class ListView(ListAPIView):
    queryset = Data.objects.all()
    serializer_class = QbSerializers

    # 过滤字段（搜索框）
    # filter_fields = ('id',)   # 只能判等

    # 使用自定义过滤类
    filter_class = MyFilter



















