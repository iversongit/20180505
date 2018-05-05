"""
Django settings for student_and_information project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(i)-_gb_!rp+*ul5&xjauxgs*)q#a142neptc4$$w()vnle3mn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'student',
    'information',
    'uauth',
    'rest_framework' # 第三方库
]

MIDDLEWARE = [   # 定义中间件
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # 阻止跨域访问、模拟操作
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'utils.UserAuthMiddleware.AuthMiddleware', # 包名 + 文件名 + 类名
    # 'utils.UserClickCountMiddleware.ClickCountMiddleware',
]

ROOT_URLCONF = 'student_and_information.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],
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

WSGI_APPLICATION = 'student_and_information.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'student_and_information',
        'USER': 'root',
        'PASSWORD': '5201314',
        'PORT': '3306'
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# 配置静态文件路径
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static')
]

# 配置上传文件(图片、视频等)路径
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# 没登陆时的跳转地址,只对加login_required的方法有用
LOGIN_URL = '/uauth/djlogin/'

# 创建日志的路径
LOG_PATH = os.path.join(BASE_DIR,'log')
if not os.path.isdir(LOG_PATH): # 判断是否有log文件夹，没有则创建
    os.mkdir(LOG_PATH)

LOGGING = {
    'version':1,
    'disable_existing_logger':False, # True: 表示禁用loggers, False:允许使用loggers
    'formatters':{ # 定义日志信息的格式
        'default':{ # key-value形式存储
            'format':'%(levelname)s %(asctime)s %(message)s' # levelno: 错误级别
        },
        'simple':{
            'format':'%(levelname)s %(module)s %(message)s'
        }
    },
    'handlers':{
        'stu_handlers':{
            'level':'DEBUG',
            # 日志文件指定为5M，超过5M重新备份，然后写入新的日志文件
            'class':'logging.handlers.RotatingFileHandler',
            # 1M=1024kb 1kb=1024b
            'maxBytes': 5 * 1024 * 1024,
            'filename': '%s/log.txt' % LOG_PATH,
            'formatter':'default'
        },
        'uauth_handlers': {
            'level': 'DEBUG',
            # 日志文件制定为5M，超过5M重新备份，然后写入新的日志文件
            'class': 'logging.handlers.RotatingFileHandler',
            # 1M=1024Kb 1kb=1024b
            'maxBytes': 5 * 1024 * 1024,
            # 文件地址
            'filename': '%s/uauth_log.txt' % LOG_PATH,
            'formatter': 'simple',
        }
    },
    'loggers':{
        'stu':{
            'handlers':{'stu_handlers'},
            'level':'INFO'
        },
        'auth':{
            'handlers':{'uauth_handlers'},
            'level':'INFO'
        }
    },
    'filters':{

    }
}

# 配置restful api返回结果
REST_FRAMEWORK = {
    # 分页
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':10, # 一页显示10条数据
    # 设置搜索
    'DEFAULT_FILTER_BACKENDS':('rest_framework.filters.DjangoFilterBackend',
                                  'rest_framework.filters.SearchFilter'),
    # 返回结构自定义
    'DEFAULT_RENDERER_CLASSES':(
        'utils.RenderResponse.CustomJsonRenderer',
    )
}