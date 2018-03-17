"""
Django settings for AlcaldeEscuchame project.

Using Django 1.11
"""
#encoding:utf-8

import os
from django_heroku.core import settings
from ctypes import cast
import posixpath
from decouple import config
import dj_database_url
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = ['testserver', 'localhost', 'alcalde-escuchame.herokuapp.com']
#ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # Add your apps here to enable them
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Own apps
    'app.apps.appConfig',
    'usuarios.apps.usuariosConfig',
    'quejas.apps.quejasConfig',
    'categorias.apps.categoriasConfig',
    'comentarios.apps.comentariosConfig',
    'corpus.apps.corpusConfig'
]

MIDDLEWARE_CLASSES = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AlcaldeEscuchame.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'AlcaldeEscuchame.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': config('DB_ENGINE'),
#        'NAME': config('DB_NAME'),
#        'USER': config('DB_USER'),
#        'PASSWORD': config('DB_PASS'),
#        'HOST': '127.0.0.1',
#	    'PORT': '5432',	# Puerto dado en pgAdmin para la BD.
#    }
#}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd1mqk8ir5nn4nj',
        'USER': 'hrfhrjlrqrykoi',
        'PASSWORD': '0c96a650abafd07226b7c6f1fc73d8fdd525a0222db8d1a0f023a33766e38598',
        'HOST': 'ec2-54-247-95-125.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}

# Extending User Model
# https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#extending-user
# AUTH_USER_MODEL = ''

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static']))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage' 

MEDIA_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['carga']))
MEDIA_URL = 'http://127.0.0.1:8000/media/'

django_heroku.settings(locals())