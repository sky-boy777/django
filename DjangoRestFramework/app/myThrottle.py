from rest_framework.throttling import SimpleRateThrottle

# 节流(反爬)
class MyThrottle(SimpleRateThrottle):
    '''('s', 'sec', 'm', 'min', 'h', 'hour', 'd', 'day')，秒，分，时，天'''
    rate = '60/m'  # 请求次数/时间（分）
    # scope = 'anon'  # 范围：匿名用户

    def get_cache_key(self, request, view):
        # 根据用户id用户名，登录不限制，不登录则限制每分钟请求次数
        if request.user and request.user.id:
            return None  # 返回None表示不限制
        else:
            return 1  # 返回其他，有限制
