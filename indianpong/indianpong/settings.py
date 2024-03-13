"""
Django settings for indianpong project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from os import environ, path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ.get("SECRET_KEY", default="w^bxst+y6yv=d*5+7h)2s3)5vfz!b2jayit+#1epn(gr1-fotw")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = environ.get("DEBUG", default=True)

ALLOWED_HOSTS = ['indianpong.com','indianpong.onrender.com', 'http://127.0.0.1:8000', 'localhost', '127.0.0.1']#environ.get("ALLOWED_HOSTS", default="").split(" ")

CSRF_TRUSTED_ORIGINS = [
    'https://indianpong.onrender.com',
    'http://indianpong.onrender.com',
]

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pong',
]

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# For production use
# you should use a more robust channel layer such as Redis.
# pip install channels_redis
""" CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
} """

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'indianpong.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'pong.context_processors.userinfo',
            ],
        },
    },
]

WSGI_APPLICATION = 'indianpong.wsgi.application'
ASGI_APPLICATION = 'indianpong.asgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
""" 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', default='pong'), 
        'USER': os.getenv('DB_USER', default='indianpong'),
        'PASSWORD': os.getenv('DB_PASSWORD', default='indianpong123'),
        'HOST': 'db',  # Değişiklik burada
        'PORT': os.getenv('DB_PORT', default='5432'),
    }
}

# For production, you should use a more robust caching backend like Memcached or Redis.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

""" DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ.get("DB_NAME", default="transcendence"),
        'USER': environ.get("DB_USER"),
        'PASSWORD': environ.get("DB_PASSWORD"),
        'HOST': environ.get("DB_HOST", default="localhost"),
        'PORT': environ.get("DB_PORT", default="5432")
    }
} """

AUTH_USER_MODEL = "pong.UserProfile"
LOGIN_URL = "login"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'
EMAIL_HOST_USER = 'indianpong@gmail.com'

""" EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = environ.get("EMAIL_HOST_USER", default="indianpong@gmail.com")
EMAIL_HOST_PASSWORD = environ.get("EMAIL_HOST_PASSWORD", default="hxog cqpq jltp xjhi")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False """

""" import certifi
environ['SSL_CERT_FILE'] = certifi.where() """