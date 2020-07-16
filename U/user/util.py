from itsdangerous import URLSafeTimedSerializer as utsr
import base64
from django.conf import settings as django_settings

# 产生token
class Token:
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.encodebytes(security_key.encode('utf-8'))
    # 生成token（加密）
    def generate_validate_token(self, uid):
        serializer = utsr(self.security_key)
        return serializer.dumps(uid, self.salt)
    # 解密
    def confirm_validte_token(self, token, expriation=3600):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expriation)
    # 移除
    def remove_validate_token(self, token):
        serializer = utsr(self.security_key)
        print(serializer.loads(token, salt=self.salt))
        return serializer.loads(token, salt=self.salt)

# 定义为全局对象， SECRET_KEY是settings.py里面的
token_confirm = Token(django_settings.SECRET_KEY)