import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '80%jf%#520^-3845iz655gc(72@urwdi-82ckaxijesy_4^ckk'

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
    'web.apps.WebConfig',
    'rest_framework',
    'rest_framework_jwt',
    # 文本编辑器
    'ckeditor',
    'ckeditor_uploader',
    # 搜索
    'haystack',
]

MIDDLEWARE = [
    # 'django.middleware.cache.UpdateCacheMiddleware',  # 添加缓存必须第一个
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',  # 读取缓存最后一个
]

ROOT_URLCONF = 'fq.urls'

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
                # 全局栏目
                'web.views.overall.arctype',
                # 归类
                'web.views.overall.aside',
            ],
        },
    },
]

WSGI_APPLICATION = 'fq.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库类型
        'NAME': 'fq',  # 数据库名字
        'HOST': 'localhost',  # ip
        'PORT': '3306',  # 端口
        'USER': 'root',  # 数据库账户
        'PASSWORD': '',  # 数据库密码
    }
}

# 数据库信息
MYDBHOST = 'localhost'
MYDBUSER = 'root'
MYDBPASS = ''
MYPORT=3306
MYDBNAME = 'fq'

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

# 静态文件
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static').replace('\\', '/')
# 上传文件
MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
CKEDITOR_UPLOAD_PATH = 'allimg/'

CACHES = {  # 缓存
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
}
CACHE_MIDDLEWARE_KEY_PREFIX = ''
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_ALIAS = 'default'

HAYSTACK_CONNECTIONS = {  # 索引路径
    'default': {
        'ENGINE': 'web.whoosh_cn_backend.WhooshEngine',  # 结合whoosh自定义
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}

# 自动更新索引文件,非必要,因为阅读量实时叠加,数据库实时更新,所以每次都生成更新索引文件,导致前端页面卡顿
# HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 20  # 指定搜索结果每页的条数
