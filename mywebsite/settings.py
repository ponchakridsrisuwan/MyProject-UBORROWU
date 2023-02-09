"""
Django settings for mywebsite project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2xo&awlx!x5gwvtsroz8wrlihqtox#3o^ct%*3x#@b8wrd1k&g'

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
    'django.contrib.sites', #new
    'allauth', #new
    'allauth.account', #new
    'allauth.socialaccount', #new
    'allauth.socialaccount.providers.google', #new
    'myapp',
    'myappstaff',
    'myappSuper',
    #'qrcode'
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

ROOT_URLCONF = 'mywebsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR/"templates",os.path.join(BASE_DIR, 'myapp/template'), os.path.join(BASE_DIR, 'myappstaff/template')
                 , os.path.join(BASE_DIR, 'myappSuper/template')],
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

WSGI_APPLICATION = 'mywebsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""

DATABASE_URL = os.environ.get('DATABASE_URL', '')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mariadb', 
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

if DATABASE_URL:
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(default=DATABASE_URL)


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'TH-th'

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'APP': {
            'client_id': '619768928773-hmql0niqevk5vc5l6l56i5o50gmdnrjj.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    }
}
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = 'none' #การยืนยันบัญชีอีเมล
LOGIN_URL = 'login' #เข้าระบบ
LOGIN_REDIRECT_URL = 'user_index' #การเปลี่ยนเส้นทาง LOGIN
LOGOUT_REDIRECT_URL = 'login_user_index' #การเปลี่ยนเส้นทาง LOGOUT
SOCIALACCOUNT_LOGIN_ON_GET = True #เข้าสู่ระบบบัญชีโซเชียล
#ACCOUNT_USER_MODEL_USERNAME_FIELD = None #ช่องข้อมูล user model ของบัญชี
#ACCOUNT_EMAIL_REQUIRED = True #ต้องมีบัญชีอีเมล
#ACCOUNT_USERNAME_REQUIRED = False #ต้องการชื่อผู้ใช้บัญชี
#ACCOUNT_AUTHENTICATION_METHOD = 'email' #วิธีการตรวจสอบบัญชี
APPEND_SLASH=False


ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_REQUIRED = True

SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_EMAIL_VERIFICATION = True #การตรวจสอบบัญชีอีเมล

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
 }