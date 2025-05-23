"""
Django settings for interest_miner_api project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import json
import logging.config
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', get_random_secret_key())
DEBUG = os.getenv('DJANGO_DEBUG', 'false').lower() == 'true'

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'django_celery_results',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'common',
    'accounts',
    'interests',
    'drf_yasg',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    #This line needs to be commented only for conference Insights and doesn't work with docker at the moment
    #'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
}

AUTH_USER_MODEL = "accounts.User"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'interest_miner_api.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ]
    },
}]

WSGI_APPLICATION = 'interest_miner_api.wsgi.application'

# Loggin configuration
LOGGING_CONFIG = None
LOGLEVEL = os.getenv('DJANGO_LOGLEVEL', 'info').upper()
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        '': {
            'level': LOGLEVEL,
            'handlers': ['console',],
        },
    },
})

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
if bool(os.environ.get("POSTGRES_HOST", False)):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get("POSTGRES_DB"),
            'USER': os.environ.get("POSTGRES_USER"),
            'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
            'HOST': os.environ.get("POSTGRES_HOST"),
            'PORT': os.environ.get("POSTGRES_PORT", 5432),
            'OPTIONS': json.loads(
                os.getenv('POSTGRES_OPTIONS', '{}')
            ),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator'
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator'
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator'
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

# No of days for which the tweets needs to be imported
TWITTER_FETCH_DAYS = int(os.getenv("TWITTER_FETCH_DAYS", 180))

# Celery settings
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
CELERY_BROKER_URL = 'redis://{}:6379'.format(REDIS_HOST)
CELERY_RESULT_BACKEND = 'redis://{}:6379'.format(REDIS_HOST)
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERYD_TASK_SOFT_TIME_LIMIT = 60 * 60  # 1 hour timeout

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
}

TEMP_DIR  = os.environ.get("TEMP_DIR",  "../tmp")
MODEL_DIR = os.environ.get("MODEL_DIR", "../model")
PRELOAD_MODELS = os.environ.get("PRELOAD_MODELS", "false").lower() == "true"

LDA_MODEL_FILE_PATH = os.path.join(
    MODEL_DIR,
    os.environ.get("LDA_MODEL_FILE", "keyword_extractor/lda-1000-semeval2010.py3.pickle.gz")
)

if os.environ.get("GLOVE_MODEL_FILE"):
    GLOVE_MODEL_FILE_PATH = os.path.join(
        MODEL_DIR,
        os.environ.get("GLOVE_MODEL_FILE")
    )
else:
    GLOVE_MODEL_FILE_PATH = None

if not os.environ.get("NLTK_DATA"):
    if os.environ.get("NLTK_MODEL_DIR"):
        os.environ["NLTK_DATA"] = os.path.join(
            MODEL_DIR,
            os.environ.get("NLTK_MODEL_DIR")
        )

if PRELOAD_MODELS:
    from interests.Semantic_Similarity.Word_Embedding.data_models import glove_model
