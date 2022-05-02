"""
Django settings for Django-CRUD-Ajax project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-bw7t11v_9=-y)=t4r87lr2+4nd(u+$=sei)jq%6w#(yh(yk+vj'

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
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'account',
    'cms',
    'app',
    'widget_tweaks',
    'django_cleanup',
    'bootstrap_datepicker_plus',
    'pwa',
    'notifications',
    'webpush',
]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path(BASE_DIR).joinpath('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app.context_processors.nav_cats',  #custom context processor

            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

def get_cache():
    import os
    try:
        servers = os.environ['MEMCACHIER_SERVERS']
        username = os.environ['MEMCACHIER_USERNAME']
        password = os.environ['MEMCACHIER_PASSWORD']
        return {
            'default': {
                'BACKEND': 'django_bmemcached.memcached.BMemcached',
                # TIMEOUT is not the connection timeout! It's the default expiration
                # timeout that should be applied to keys! Setting it to `None`
                # disables expiration.
                'TIMEOUT': None,
                'LOCATION': servers,
                'OPTIONS': {
                    'binary': True,
                    'username': username,
                    'password': password,
                    'behaviors': {
                        # Enable faster IO
                        'no_block': True,
                        'tcp_nodelay': True,
                        # Keep connection alive
                        'tcp_keepalive': True,
                        # Timeout settings
                        'connect_timeout': 2000,  # ms
                        'send_timeout': 750 * 1000,  # us
                        'receive_timeout': 750 * 1000,  # us
                        '_poll_timeout': 2000,  # ms
                        # Better failover
                        'ketama': True,
                        'remove_failed': 1,
                        'retry_timeout': 2,
                        'dead_timeout': 30,
                    }
                }
            }
        }
    except:
        return {
            'default': {
                'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
                'LOCATION': '127.0.0.1:11211',
                'OPTIONS': {
                    'no_delay': True,
                    'ignore_exc': True,
                    'max_pool_size': 4,
                    'use_pooling': True,
                }
            }
        }


CACHES = get_cache()

SELECT2_CACHE_BACKEND = "default"

# SELECT2_JS = '/static/django_select2/select2.min.js'
# SELECT2_CSS = '/static/django_select2/select2.min.css'

AUTH_USER_MODEL = "account.User"
 
LOGIN_URL = 'account:login'

LOGOUT_URL = 'account:logout'

LOGIN_REDIRECT_URL = '/'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # During development only

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'richrein14@gmail.com'
EMAIL_HOST_PASSWORD = 'rein144440'
# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = Path(BASE_DIR).joinpath('staticfiles')

STATICFILES_DIRS = [Path(BASE_DIR).joinpath('static')]

MEDIA_URL = '/media/'

MEDIA_ROOT = Path(BASE_DIR).joinpath('media')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

WHITENOISE_MAX_AGE = 31536000

# Bootstrap 4 message tags and class.
from django.contrib import messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "BCJeqkLUG8eykeModZxnS_62LnEfvrTaDpCjlTjwd7PWCqYQVK_2s833kYZFPFLgwiX3g8zg4DMp9m6aQ_kBdas",
    "VAPID_PRIVATE_KEY": "2c_by4BIlzAEtlps-DGUUW-6zb16OD__C0909JX0sUU",
    "VAPID_ADMIN_EMAIL": "richrein14@gmail.com"
}

PWA_APP_NAME = 'My App'
PWA_APP_DESCRIPTION = "My app description"
PWA_APP_THEME_COLOR = '#0A0302'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': '/static/images/my_app_icon.png',
        'sizes': '160x160'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/images/my_apple_icon.png',
        'sizes': '160x160'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/images/icons/splash-640x1136.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'
import os
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static/js', 'serviceworker.js')
