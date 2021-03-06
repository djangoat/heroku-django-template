"""
Django settings for {{ project_name }} project.

Generated by 'django-admin startproject' using Django {{ django_version }}.

For more information on this file, see
https://docs.djangoproject.com/en/{{ docs_version }}/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/
"""


import os
import dj_database_url

from dotenv import load_dotenv, find_dotenv
from django.contrib.messages import constants as message_constants

from sentry_sdk import init as sentry_sdk_init
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# for local development: see https://github.com/theskumar/python-dotenv
load_dotenv(find_dotenv())

# Crude way of detecting if we are currently running on heroku or not...
HEROKU = os.getenv('PYTHONPATH') and '.heroku' in os.getenv('PYTHONPATH')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', "{{ secret_key }}")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', False)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Disable Django's own staticfiles handling in favour of WhiteNoise, for
    # greater consistency between gunicorn and `./manage.py runserver`. See:
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.redirects',
    'django_extensions',
    'debug_toolbar',
    'admin_honeypot',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
]

ROOT_URLCONF = '{{ project_name }}.urls'

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
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = '{{ project_name }}.wsgi.application'

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
# https://docs.djangoproject.com/en/{{ docs_version }}/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.getenv('TIMEZONE', 'UTC')
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
if HEROKU:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Remove this when using a multi site layout
SITE_ID = 1

# This should be turned on in production applications
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', False)

# Secures the admin path by sending to the honeypot by default
ADMIN_PATH = os.getenv('ADMIN_PATH', '{% lorem 1 w random %}')

# Enables the django-debug-toolbar for local dev only
INTERNAL_IPS = ['127.0.0.1']

# Bootstrapify the message tags
MESSAGE_TAGS = {
    message_constants.DEBUG: 'debug',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger',
}

# In case you need mail...
MAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_PORT = os.getenv('EMAIL_PORT')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# sentry.io
ENVIRONMENT = os.getenv('ENVIRONMENT', 'local')
SENTRY_ENVIRONMENT = os.getenv('SENTRY_ENVIRONMENT', ENVIRONMENT)
# Sentry
if 'SENTRY_DSN' in os.environ:
    sentry_sdk_init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[
            DjangoIntegration(),
        ],
        environment=SENTRY_ENVIRONMENT,
    )

# Travis
if 'TRAVIS' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'test',
            'USER': 'postgres',
            'HOST': 'localhost',
            'PORT': 5432,
        }
    }

# Celery
REDIS_URL = os.getenv('REDIS_URL')
BROKER_URL = os.getenv('BROKER_URL', REDIS_URL)
CELERY_TASK_ALWAYS_EAGER = os.getenv('CELERY_TASK_ALWAYS_EAGER', DEBUG)


##################################################################################
# Static files (CSS, JavaScript, Images)                                         #
# https://docs.djangoproject.com/en/{{ docs_version }}/howto/static-files/       #
##################################################################################

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

if HEROKU:
    # Ensure STATIC_ROOT exists.
    os.makedirs(STATIC_ROOT, exist_ok=True)


##################################################################################
# Database                                                                       #
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#databases   #
##################################################################################

# SQLITE environment as default for local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Change 'default' database configuration with $DATABASE_URL.
# It is hard to do locally so change here as appropriate
DB_SSL_REQUIRE = os.getenv('DB_SSL_REQUIRE', HEROKU)
DB_CONN_MAX_AGE = os.getenv('DB_CONN_MAX_AGE', 600)
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES['default'].update(
        dj_database_url.config(
            conn_max_age=DB_CONN_MAX_AGE,
            ssl_require=DB_SSL_REQUIRE,
        )
    )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
}
