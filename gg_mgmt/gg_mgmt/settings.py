# -*- coding: utf-8 -*-

"""
Django settings for gg_mgmt project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#7u+-4l800juo6b#h+jg1d=qgn)akt9m(3uo18#*b=56%dpyyh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [u'localhost', u'127.0.0.1', u'192.168.1.45', u'www.ggzs.me', u'ggzs.me', u'106.187.54.178']

LOGIN_URL = '/gg_mgmt/accounts/login/'

LOGOUT_URL = '/gg_mgmt/accounts/logout/'

LOGIN_REDIRECT_URL = '/gg_mgmt/accounts/profile/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # 'templates',
    os.path.join(BASE_DIR, 'templates'),
  #  os.path.join(BASE_DIR, 'm_templates'),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'forum',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'gg_mgmt.urls'

WSGI_APPLICATION = 'gg_mgmt.wsgi.application'

#给不同的app制定对应的database
DATABASE_ROUTERS = ['dbsetings.appdb']
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'admin',
            'USER': 'root',
            'PASSWORD': '111111',
            'HOST': '192.168.1.45',
            'PORT': '3306'
        },
        'forum': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'forum',
            'USER': 'root',
            'PASSWORD': '111111',
            'HOST': '192.168.1.45',
            'PORT': '3306'
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'admin',
            'USER': 'forum',
            'PASSWORD': 'VQq*d@GY4F7J6]MP',
            'HOST': 'localhost',
            'PORT': '3306'
        },
        'forum': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'forum',
            'USER': 'forum',
            'PASSWORD': 'VQq*d@GY4F7J6]MP',
            'HOST': 'localhost',
            'PORT': '3306'
        },
    }


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ('img', os.path.join(STATIC_ROOT, 'img').replace('\\', '/')),
    ('css', os.path.join(STATIC_ROOT, 'css').replace('\\', '/')),
    ('js', os.path.join(STATIC_ROOT, 'js').replace('\\', '/')),
    ('AdminLTE/bootstrap', os.path.join(STATIC_ROOT, 'AdminLTE/bootstrap').replace('\\', '/')),
    ('AdminLTE/dist', os.path.join(STATIC_ROOT, 'AdminLTE/dist').replace('\\', '/')),
    ('AdminLTE/plugins', os.path.join(STATIC_ROOT, 'AdminLTE/plugins').replace('\\', '/')),
)

if DEBUG:
    LOG_DIR = '/var/log/gg_mgmt'
else:
    LOG_DIR = '/var/log/gg_mgmt'

# logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(name)s %(asctime)s %(message)s'
        },
        'verbose': {
            'format': '%(levelname)s %(name)s %(asctime)s %(pathname)s %(module)s %(lineno)d %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'django_request': {
            'format': '%(levelname)s %(asctime)s %(pathname)s %(module)s %(lineno)d %(message)s status_code:%(status_code)d',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'django_db_backends': {
            'format': '%(levelname)s %(asctime)s %(pathname)s %(module)s %(lineno)d %(message)s duration:%(duration).3f sql:%(sql)s params:%(params)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'custom_log_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django.log'),
            'backupCount': 5,
            'maxBytes': '16777216',  # 16megabytes(16M)
            'formatter': 'verbose'
        },
        'django_request_logfile': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django_request_logfile.log'),
            #you need define your VAR_ROOT variable that points to your project path,and mkdir a logs directory in your project root path.
            'backupCount': 5,
            'maxBytes': '16777216',  # 16megabytes(16M)
            'formatter': 'django_request'
        },
        'django_db_backends_logfile': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django_db_backends_logfile.log'),
            #you need define your VAR_ROOT variable that points to your project path,and mkdir a logs directory in your project root path.
            'backupCount': 5,
            'maxBytes': '16777216',  # 16megabytes(16M)
            'formatter': 'django_db_backends'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'error': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'backupCount': 5,
            'maxBytes': '16777216',  # 16megabytes(16M)
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['custom_log_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins', 'django_request_logfile'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['django_db_backends_logfile', ],
            'level': 'WARNING',
            'propagate': True,
        },
        'error': {
            #then you can change the level to control your custom app whether to output the debug infomation
            'handlers': ['error'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
