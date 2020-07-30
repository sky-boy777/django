from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

# 自定义验证类,身份验证本身不会允许或不允许传入的请求，它只会标识发出请求的凭据,告诉你验证是否通过，其他还会继续执行
class MyAuthentications(BaseAuthentication):
    # 必须重写authenticate方法
    def authenticate(self, request):
        # 获取token
        token = request.query_params.get('token')  # query_params等于GET
        # 验证token
        if token == 'abcd':
            print('验证成功')
            return None  # 必须返回一个元组,第二个参数可以是None
        else:
            print('验证不成功')
            # 验证不成功直接返回
            raise AuthenticationFailed('验证不成功')
            # 如果return None则会继续执行请求
            # return None