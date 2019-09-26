# 生产环境/线上配置

"""
Django settings for meiduo_mall project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os, sys

# print(sys.path)
# ['/home/python/Desktop/meiduo_project/meiduo_mall',
# '/home/python/Desktop/meiduo_project/meiduo_mall',
# '/snap/pycharm-professional/151/helpers/pycharm_display',
# '/home/python/.virtualenvs/meiduo_mall/lib/python36.zip',
# '/home/python/.virtualenvs/meiduo_mall/lib/python3.6',
# '/home/python/.virtualenvs/meiduo_mall/lib/python3.6/lib-dynload',
# '/usr/lib/python3.6', '/home/python/.virtualenvs/meiduo_mall/lib/python3.6/site-packages',
# '/snap/pycharm-professional/151/helpers/pycharm_matplotlib_backend']

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 追加项目导包路径
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
# print(sys.path)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(&!uryi+5w+g065l^zqfap28a1!0uhl@br(ifmd**9rm*tkyzk'

# SECURITY WARNING: don't run with debug turned on in production!
# 默认开启调试模型 上线时需要设置为False ,Django就不再提供静态文件访问服务
DEBUG = False

# 允许哪些域名来访问django
ALLOWED_HOSTS = ['www.meiduo.site', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'haystack',  # 全文检索
    'django_crontab',  # 定时任务

    'users.apps.UsersConfig',  # 用户模块
    'oauth.apps.OauthConfig',  # QQ模块
    'areas.apps.AreasConfig',  # 省市区模块
    'contents.apps.ContentsConfig',  # 首页模块
    'goods.apps.GoodsConfig',  # 商品模块
    'order.apps.OrderConfig', # 订单模块
    'payment.apps.PaymentConfig' #支付模块
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meiduo_mall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',  # 更改模板引擎为jinja2
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # 补充Jinja2模板引擎环境
            'environment': 'meiduo_mall.utils.jinja2_env.jinja2_environment',
        },
    },
]

WSGI_APPLICATION = 'meiduo_mall.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, '../../db.sqlite3'),
#     }
# }
DATABASES = {
    'default': { # 主机：增删改， 写入
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 3306,  # 数据库端口
        'USER': 'root',  # 数据库用户名
        'PASSWORD': 'mysql',  # 数据库用户密码
        'NAME': 'meiduo'  # 数据库名字
    },
    'slave': {  # 丛机: 查 读
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 8306,  # 数据库端口
        'USER': 'meiduo',  # 数据库用户名
        'PASSWORD': 'meiduo',  # 数据库用户密码
        'NAME': 'meiduo'  # 数据库名字
    },
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

# LANGUAGE_CODE = 'en-us'
#
# TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# 配置项目缓存为redis缓存
CACHES = {
    "default": {  # 默认
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {  # session
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "verify_code": {  # 验证码
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "history": {  # 用户浏览记录
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "carts": {  # 购物车数据
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/4",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), 'logs/meiduo.log'),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}

# 指定认证系统模型
AUTH_USER_MODEL = 'users.User'

# 指定自定义的用户认证后端
AUTHENTICATION_BACKENDS = ['users.utils.UsernameMobileAuthBackend']

# 修改登录界面路由
LOGIN_URL = '/login/'

# QQ登录参数
# QQ_CLIENT_ID = '101518219'
# QQ_CLIENT_SECRET = '418d84ebdc7241efb79536886ae95224'
# QQ_REDIRECT_URI = 'http://www.meiduo.site:8000/oauth_callback'
# QQ登录参数 #（生产环境）
QQ_CLIENT_ID = '101531904'
QQ_CLIENT_SECRET = '6afc7211294442e13439b5b4b7ae9118'
QQ_REDIRECT_URI = 'http://www.meiduo.site:80/oauth_callback'

# 发送邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 指定邮件后端
EMAIL_HOST = 'smtp.163.com'  # 发邮件主机
EMAIL_PORT = 25  # 发邮件端口
EMAIL_HOST_USER = 'itcast99@163.com'  # 授权的邮箱
EMAIL_HOST_PASSWORD = 'python99'  # 邮箱授权时获得的密码，非注册登录密码
EMAIL_FROM = '美多商城<itcast99@163.com>'  # 发件人抬头

# 邮箱验证链接
# EMAIL_VERIFY_URL = 'http://www.meiduo.site:8000/emails/verification/'

EMAIL_VERIFY_URL = 'http://www.meiduo.site/emails/verification/'

# 指定远程图片下载位置
# MEDIA_URL = 'http://192.168.233.131:8888/'

# 指定自定义文件存储类
DEFAULT_FILE_STORAGE = 'meiduo_mall.utils.fastdfs.fdfs_storage.FastDFSStorage'

# 指定fastdfs域名和端口
FDFS_BASE_URL = 'http://image.meiduo.site:8888/'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://192.168.233.131:9200/', # Elasticsearch服务器ip地址，端口号固定为9200
        'INDEX_NAME': 'meiduo_mall', # Elasticsearch建立的索引库的名称
    },
}

# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 支付宝
ALIPAY_APPID = '2016101300676300'
ALIPAY_DEBUG = True  # 表示是沙箱环境还是真实支付环境
ALIPAY_URL = 'https://openapi.alipaydev.com/gateway.do'
ALIPAY_RETURN_URL = 'http://www.meiduo.site/payment/status/'

# 定时器任务
CRONJOBS = [
    # 每1分钟生成一次首页静态文件
    ('*/1 * * * *', 'contents.crons.generate_static_index_html', '>> ' + os.path.join(os.path.dirname(BASE_DIR), 'logs/crontab.log'))
]

# 解决定时器中文编码问题
CRONTAB_COMMAND_PREFIX = 'LANG_ALL=zh_cn.UTF-8'

# 数据库路由
DATABASE_ROUTERS = ['meiduo_mall.utils.db_router.MasterSlaveDBRouter']

# 静态文件收集目录
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')