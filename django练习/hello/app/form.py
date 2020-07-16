from django import forms
from captcha.fields import CaptchaField

# 验证码类
class CaptchaTestForm(forms.Form):
    captcha = CaptchaField()  # 验证码字段


# 表单类(表单提交过来的跟这里要一致)
class RegisterForm(forms.Form): # 最大长度      # 不能为空       # 提示的错误信息
    username = forms.CharField(max_length=15, required=True, error_messages={
        'required': '用户名不能为空',
        'max_length': '用户名长度不能超过15给字符'
    })
    password = forms.CharField(min_length=3, required=True, error_messages={
        'required': '密码不能为空',
        'max_length': '密码长度不能少于三个字符'
    })

    # # 单个字段验证clean_xxxxx
    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     if len(password) < 3:
    #         raise ValueError('密码长度不够')
    #     return password

    # # 多个字段验证
    # def clean(self):
    #      .......
    #     password = self.cleaned_data.get('password')

