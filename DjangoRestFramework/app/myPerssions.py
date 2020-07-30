from rest_framework.permissions import BasePermission

# 自定义权限类
class MyPerssion(BasePermission):
    # 对视图
    def has_permission(self, request, view):
        print('权限')
        return True  # 返回True则通过，返回False则不通过

        # 如果登录了，则通过
        # return request.user

    def has_object_permission(self, request, view, obj):
        '''权限规则自定'''
        return True  # 同上

