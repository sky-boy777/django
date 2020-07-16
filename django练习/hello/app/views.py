from django.shortcuts import render, redirect,reverse
from django.http import HttpResponse,HttpResponseRedirect
from app.models import User
import datetime
from app.form import CaptchaTestForm, RegisterForm

# Create your views here.
def index(request):
	# 尝试获取cookie(大写),指定键值对
	# username = request.COOKIES.get('username')

	# 获取session
	username = request.session.get('username')
	u = request.session.get('xxx')

	return render(request, 'index.html', {'username': username})  # locals()

def login(request):
	if request.method == 'POST':
		# 登录
		# username = request.POST.get('username')
		# password = request.POST.get('password')

		userinfo = request.POST.dict()  # 以字典的形式接受提交过来的数据
		userinfo.pop('csrfmiddlewaretoken')  # 弹出其他键值对
		# user = User.objects.filter(username=userinfo.get('username'), password=userinfo.get('password')).first()
		user = User.objects.filter(**userinfo).first()  # 解包查询（username=username, password=password）

		# 如果查询到数据就设置cookies
		if user:
			# res = redirect('/')  # 需要一个响应对象，HttpResponse也是,然后跳转到首页
			# # 设置cookie跟过期时间(登录后3小时后过期)
			# cookies_time = datetime.datetime.now() + datetime.timedelta(hours=3)
			# res.set_cookie('username', user.username, expires=cookies_time)  # 设置cookie
			# return res

			# 设置session,可以设置多个
			request.session.set_expiry(0)  # 过期时间（秒），0表示浏览器关闭
			request.session['username'] = user.username
			# request.session['xxx'] = 'dfjsfksldkfsfjsfkjk'
			return redirect('app:index')

	return render(request, 'login.html')

def logout(request):
	# 删除cookie要先创建一个响应对象
	# res = HttpResponse()
	# res = redirect('app:login')
	# res.delete_cookie('username')
	# return res    # 或者HttpResponse('ko')

	# 删除session
	request.session.clear()  #清除所有session键值对，不清除sessionid
	# request.session.flush()   # 清除所有session键值对，连数据库里面的也清除
	# del request.session['username']  # 清除指定session键值对


	return redirect('app:login')



# 注册+表单验证
def register(request):
	# post请求表示提交数据注册
	if request.method == 'POST':

		# 提交过来的数据生成表单
		form = RegisterForm(request.POST)
		# 验证表单有没有错误，没有为True，然后进行注册处理
		if form.is_valid():

			# 业务处理（注册）(以下是获取表单的几种形式)
			# 1
			username = request.POST.get('username')
			password = request.POST.get('password')

			# 2
			# username = form.cleaned_data.get('username', '')
			# password = form.cleaned_data.get('password', '')

			# 3
			#data = request.POST.dict()

			# 保存到数据库
			user = User.objects.create(username=username, password=password)
			# user = User()
			# user.username = username
			# user.password = password
			# user.save()

			# 重定向到登录页面
			return redirect('app:login')
		else:
			# 验证不成功将错误信息返回，渲染到页面
			return render(request, 'register.html', {'form': form})

	# get请求表示来到注册页面
	return render(request, 'register.html')
	
	# return JsonRespose()  返回json数据
	# 重定向
	# 原生sql user.objects.raw(sql语句)


# 装饰器保护路由(写在被装饰函数前面)
def check_login(fn):
	def inner(*args, **kwargs):  # 这个就是被装饰的函数 args[0]-->request,也就是第一个参数
		if args[0].COOKIES.get('username'):
			return fn(*args, **kwargs)  # 里面有返回值，跟被装饰的函数要一样，返回值跟参数
		else:
			return redirect('app:login')  # 注意要有返回值
	return inner


# 需要登录才能访问的页面
@check_login
def user(request):
	return render(request, 'user.html')

# 验证码
def cap(request):
	if request.method == 'POST':
		form = CaptchaTestForm(request.POST)
		if form.is_valid():
			print('验证通过')
		else:
			print("输入错误")
	form = CaptchaTestForm()
	return render(request, 'app/yam.html', locals())


