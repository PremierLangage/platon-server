"""Django settings for platon project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys
import hashlib
import logging
from datetime import timedelta

import dj_database_url

################################################################################
#                              Django's Settings                               #
################################################################################

# Filebrowser settings
FILEBROWSER_DISALLOWED_CHAR = ['/', ' ', '\t', '\n', ';', '#', '+', '&']

# Directories
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SETTINGS_DIR)
APPS_DIR = os.path.realpath(os.path.join(BASE_DIR, "apps"))

# NFS Directory settings
NFS_DISK = os.path.join(BASE_DIR, '../disk-nfs')
if not os.path.isdir(NFS_DISK):
    os.makedirs(NFS_DISK)

# Directory where assets are stored
ASSETS_ROOT = os.path.join(NFS_DISK, 'assets')
if not os.path.isdir(ASSETS_ROOT):
    os.makedirs(ASSETS_ROOT)

# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    '-90k)h+jqn8^82(om*zr(1dl^39kr4g&0_84bsdaueo7u6+)s+'
).strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'false').strip().lower() == 'true')

# Set to true when 'python3 manage.py test' is used
TESTING = sys.argv[1:2] == ['test']

# Allowed Hosts
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').strip().split(',')

if not TESTING:
    # https://stackoverflow.com/questions/8153875/how-to-deploy-an-https-only-site-with-django-nginx
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition
PREREQ_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.postgres',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'channels',
    'django_celery_beat',
    'django_extensions',
    'django_elasticsearch_dsl',
    'django_elasticsearch_dsl_drf',
    'django_filters',
    'rest_framework',
    'notifications',
]

PROJECT_APPS = [
    'pl_auth',
    'pl_core',
    'pl_lti',
    'pl_users',
    'pl_sandbox',
    'pl_resources',
    'pl_notifications',
    'pl_loader',
    'pl_asset',
    'pl_live',
]


INSTALLED_APPS = PREREQ_APPS + THIRD_PARTY_APPS + PROJECT_APPS

# Middleware Definition
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    # App middlewares
    'pl_lti.middleware.LTIAuthMiddleware',
]

if DEBUG and not TESTING:
    # https://django-debug-toolbar.readthedocs.io/en/stable/index.html
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
    DEBUG_TOOLBAR_CONFIG = {
        # Toolbar options
        'RESULTS_CACHE_SIZE': 3,
        'SHOW_COLLAPSED': True,
        'SHOW_TOOLBAR_CALLBACK': lambda _: True,
        # Panel options
        'SQL_WARNING_THRESHOLD': 100,   # milliseconds
    }

# URL
ROOT_URLCONF = 'platon.urls'

# Template definition
TEMPLATES = [
    {
        'BACKEND':  'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'shared/templates')
        ],
        'APP_DIRS': True,
        'OPTIONS':  {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Email
# Used by mail_admins log handler,
# set ENABLE_MAIL_ADMINS to True to use it (DEBUG should also be set to False)
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
SERVER_EMAIL = 'root@localhost'
ADMINS = []
# Write email in console instead of sending it if DEBUG is True
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Logging definition
LOGGING = {
    'version':                  1,
    'disable_existing_loggers': False,
    'filters':                  {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true':  {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters':               {
        'verbose': {
            'format':  '[%(asctime)-15s] %(levelname)s -- '
                       'File: %(pathname)s line n°%(lineno)d -- %(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S'
        },
        'simple':  {
            'format':  '[%(asctime)-15s] %(levelname)s -- %(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S'
        },
    },
    'handlers':                 {
        'console':     {
            'level':     'DEBUG',
            'filters':   ['require_debug_true'],
            'class':     'logging.StreamHandler',
            'formatter': 'simple'
        },
        'syslog': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'local7',
            'address': '/dev/log' if os.path.exists('/dev/log') else '/var/run/syslog',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level':        'ERROR',
            'class':        'django.utils.log.AdminEmailHandler',
            'include_html': True,
            'formatter':    'verbose'
        }
    },
    'loggers':                  {
        '': {
            'handlers': ['console', 'mail_admins'],
            'level':    'INFO',
        },
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level':    'ERROR',
        }
    },
}


WSGI_APPLICATION = 'platon.wsgi.application'
ASGI_APPLICATION = 'platon.routing.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     os.getenv('DB_NAME', 'django_platon').strip(),
        'USER':     os.getenv('DB_USERNAME', 'django').strip(),
        'PASSWORD': os.getenv('DB_PASSWORD', 'django_password').strip(),
        'HOST':     os.getenv('DB_HOST', '127.0.0.1').strip(),
        'PORT':     os.getenv('DB_PORT', '5432').strip(),
    }
}
# https://docs.djangoproject.com/en/3.2/releases/3.2/#customizing-type-of-auto-created-primary-keys
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)


# Authentication

LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = '/'

# https://docs.djangoproject.com/fr/3.2/topics/auth/customizing/#substituting-a-custom-user-model
AUTH_USER_MODEL = 'pl_users.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'pl_lti.backends.LTIAuthBackend',
)


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# JWT
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Django Rest Framework
# https://www.django-rest-framework.org

DEFAULT_RENDERER_CLASSES = (
    'rest_framework.renderers.JSONRenderer',
)

if DEBUG:  # remove browable api in prod
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.

    # https://www.django-rest-framework.org/api-guide/renderers/#api-reference
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES,
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    # https://www.django-rest-framework.org/api-guide/parsers/#api-reference
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    # https://www.django-rest-framework.org/api-guide/authentication/#api-reference
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # https://www.django-rest-framework.org/api-guide/permissions/#api-reference
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'PAGE_SIZE': 100,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}


# Elasticsearch
# https://django-elasticsearch-dsl.readthedocs.io/en/latest/settings.html

ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', '127.0.0.1').strip()
ELASTICSEARCH_PORT = os.getenv('ELASTICSEARCH_PORT', '9200').strip()

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': f'{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}'
    },
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = 'fr-FR'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'static'))
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "shared/static"),
]

MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'media'))
MEDIA_URL = '/media/'

################################################################################
#                             Third-Party's Settings                           #
################################################################################

# Channel layer

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1').strip()
REDIS_PORT = os.getenv('REDIS_PORT', '6379').strip()

# https://channels.readthedocs.io/en/latest/topics/channel_layers.html
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG':  {
            "hosts": [(REDIS_HOST, int(REDIS_PORT))],
        },
    },
}

# Celery

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Paris'

################################################################################
#                            Project's Settings                                #
################################################################################

# Sandbox's settings
####################
# Seconds between polls of sandboxes usage. Must not be less than 30.
SANDBOX_POLL_USAGE_EVERY = 15
# Seconds between polls of sandboxes specifications. Must not be less than 300.
SANDBOX_POLL_SPECS_EVERY = 60 * 10
# Default sandbox url
SANDBOX_URL = os.getenv('SANDBOX_URL', 'http://localhost:7000/')
################################################################################

# Directories
DIRECTORIES_ROOT = os.path.join(BASE_DIR, "directories")

# Identicon (default avatar)
IDENTICON_OPTIONS = {
    'background':    'rgb(224,224,224)',
    'foreground':    [
        'rgb(45,79,255)',
        'rgb(254,180,44)',
        'rgb(226,121,234)',
        'rgb(30,179,253)',
        'rgb(232,77,65)',
        'rgb(49,203,115)',
    ],
    'row':           15,
    'col':           15,
    'padding':       (20, 20, 20, 20),
    'size':          (300, 300),
    'digest':        hashlib.sha1,
    'output_format': 'png',
}

if APPS_DIR not in sys.path:  # pragma: no cover
    sys.path.append(APPS_DIR)


try:
    from .config import *
except Exception:
    if "VERBOSE" in os.environ:
        logger = logging.getLogger(__name__)
        logger.exception("No config file found.")
    pass
