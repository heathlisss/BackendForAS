"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-e7&cvcmtmdgdf)e#0)f0f#5f=5f(f#0%^-xf3qg8y!m#l!+9(%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []



# Application definition

INSTALLED_APPS = [
    "surveys.apps.SurveysConfig",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',  # JSON-рендеринг для API
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
}



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        'NAME': 'surveys',
        'USER': 'postgres',
        'PASSWORD': '1440',
        'HOST': 'db_survey',
        'PORT': '5000',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]


JWT_SECRET_KEY = "597207f868467ef08e3d3c2fe1c5d0457477b6246372e39f081160949ca6debbd60542470d424483a73a34351ff5f658508e79be48e1fbeb4fdd543616573908043e1fe970f49d239fd37646acdbd61620cd95f77715d33f798b3970b83b55feb6cf04d89fbdf24fd4f7ba0d8f1c70f118d1b853370c18ceb508a48991d976694f9a44e04892aec27ef6edb84e806d7535ac92b7e32bcaf7f4ca5d424798fdbed27ecc44c4a84ea10240f5caec746815423290111f1a95cd0414cde1251d2a98a6e7ea74d0aae2d44dd54f6f91294d054fa1c41873b0d2f1a909a71088e1958e9fc0c44177596daf912ab89973730f2131d68bc985594a3fea4e584d5241d3b669f5720a059bf66f21b33177ed9bd2853bbcd39874adb526acf27001146413c19e339392eeda4fc3efeb60c109f6f730321fcb3b277373a6855e8d2a80763f3209ad4de242946c1b163194df9860d2b2e1b4c7cc9aab757cd06e9ff2495e7cb0e0e4bdd79bef207d419234666ba60d2e72c567a93998e0b2ee42d9f50a8be3514fa85f80f792f29449db896684c619dda8ea5de6349ee4e1067f2ef8ed4a14940b2080c2acf4199e0976831925deac8a249300eb544dc9311d198af4644f41f08a57da870dd92c7aac0b1c3dc9787914bc1f3a7ed62616e948312b108048955505a29befb08caee201b0902dc33cecec5d044de2dbaa5a3c071293e989d64d13"
JWT_ALGORITHM = "HS256"
