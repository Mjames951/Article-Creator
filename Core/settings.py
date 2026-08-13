from pathlib import Path
import os
import environ


env = environ.Env()

IMG_MAX_WIDTH_HEIGHT = 500

SITE_ID = 1 
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_URL = 'localhost'

environ.Env.read_env(BASE_DIR / '.env', overwrite=True)

DEBUG = env.bool('DEBUG')

SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_NAME = 'articlecreator'
CSRF_COOKIE_SECURE = not DEBUG
SECRET_KEY = env.str('SECRET_KEY')

ALLOWED_HOSTS = ['localhost']
if DEBUG:
    ALLOWED_HOSTS.append('127.0.0.1')

#PRODUCTION: INCLUDE THE ACTUAL HTTPS:// NAME OF THE SERVER
CSRF_TRUSTED_ORIGINS = []

INSTALLED_APPS = [
    'storages',
    'ArticleCreator',
    'django_extensions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
    }
}