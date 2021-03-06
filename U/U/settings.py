"""
Django settings for U project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# 已改过
SECRET_KEY = 'sfa8478943j240fa732434378ee^%#%^^(&JJIUI*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 我的app
    'user',
    # 富文本框
    'tinymce',
]


MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 自定中间件
    'user.MyMiddieware.MyMiddieware',

]


ROOT_URLCONF = 'U.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'U.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'u',
        'PASSWORD': 'root',
        'USER': 'root',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'



# 静态文件夹
STATICFILSE_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# 用户认证
AUTH_USER_MODEL = 'user.User'



# 发送邮件
# 次要
# EMAIL_USE_SSL = True 或EMAIL_USE_TLS = True 控制是否安全连接，只能有一个
# EMAIL_PORT = 666   smtp服务的端口号
EMAIL_FROM = '我的信息<1251779123@qq.com>'   # 收件人看到的发送者名称，没有默认是EMAIL_HOST_USER
# 必须
EMAIL_HOST = 'smtp.qq.com'  # smtp服务的邮箱服务器， 如果是 163 改成 smtp.163.com
EMAIL_HOST_USER = '1251779123@qq.com'  # 发送邮件的邮箱
EMAIL_HOST_PASSWORD = 'fxnracpskvdfhhab'  # 开启SMTP后的客户端授权码


# 数据库缓存配置，然后python manage.py createcachetable生成缓存表
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        # 缓存表的名字
        'LOCATION': 'my_cache_table'
    }
}

# redis做缓存
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://192.168.1.101:6379/2',  # redis地址（无密码），后面表示使用第二个数据库
#         # 'LOCATION': 'redis://密码@192.168.1.101:6379/2',  # redis地址（有密码），后面表示使用第二个数据库
#     }
# }
