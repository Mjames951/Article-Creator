from pathlib import Path
import os
import environ


env = environ.Env()

IMG_MAX_WIDTH_HEIGHT = 500


BASE_DIR = Path(__file__).resolve().parent.parent
BASE_URL = 'https://planetplum.fly.dev'

environ.Env.read_env(BASE_DIR / '.env', overwrite=True)

DEBUG = env.bool('DEBUG')
SITE_ID = env.int('SITE_ID')

SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_NAME = 'plum'
CSRF_COOKIE_SECURE = not DEBUG
SECRET_KEY = env.str('SECRET_KEY')

#PRODUCTION: INCLUDE THE ACTUAL NAME OF THE FLY.IO SERVER
APP_NAME = os.environ.get("FLY_APP_NAME")
ALLOWED_HOSTS = ['localhost', 'planetplum.net', f"{APP_NAME}.fly.dev"]
if DEBUG:
    ALLOWED_HOSTS.append('127.0.0.1')

#PRODUCTION: INCLUDE THE ACTUAL HTTPS:// NAME OF THE FLY.IO SERVER
CSRF_TRUSTED_ORIGINS = ['https://planetplum.net', 'https://*.fly.dev']

INSTALLED_APPS = [
    'storages',
    'users',
    'shop',
    'plum',
    'blog',
    'django_extensions',
    'django.contrib.admin',
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
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'storemain.urls'

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

WSGI_APPLICATION = 'storemain.wsgi.application'

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        'default': env.db(), 
    }


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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'

AUTH_USER_MODEL = "users.CustomUser"
AUTHENTICATION_BACKENDS = ['users.authentication.BackendAuth']

STRIPE_KEY = env('STRIPE_KEY')

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_ENDPOINT_URL_S3 = env('AWS_ENDPOINT_URL_S3')
AWS_ENDPOINT_URL_IAM = env('AWS_ENDPOINT_URL_IAM')
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = True
AWS_QUERYSTRING_EXPIRE = 400000
AWS_S3_FILE_OVERWRITE = False
AWS_LOCATION = 'plum' 



if not DEBUG:
    #PRODUCTION
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3.S3Storage",
        },
    }
else:
    STATIC_URL = '/static/'
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        }
    }



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False