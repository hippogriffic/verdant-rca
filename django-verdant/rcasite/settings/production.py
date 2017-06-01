import os
import dj_database_url
import raven

from .base import *  # noqa

# Do not set SECRET_KEY, Postgres or LDAP password or any other sensitive data here.
# Instead, use environment variables or create a local.py file on the server.

# Disable debug mode
DEBUG = False


# Use cached template loader
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)


# Send emails from publications@rca.ac.uk via gmail.com
DEFAULT_FROM_EMAIL = 'publications@rca.ac.uk'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL
EMAIL_HOST_PASSWORD = ''


# LDAP authentication
from rca_ldap.settings import *

AUTH_LDAP_BIND_DN = ''
AUTH_LDAP_BIND_PASSWORD = ''
AUTH_LDAP_SERVER_URI = ''

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)


# Google Analytics
GOOGLE_ANALYTICS_ACCOUNT = 'UA-3809199-5'

SILVERPOP_ID = 'd871c05-15671ce6a9e-c6f842ded9e6d11c5ffebd715e129037'
SILVERPOP_BRANDEDDOMAINS = 'www.pages05.net,rcawebsite,studentenquiry97.mkt4116.com'


# Compress static files offline and minify CSS
# http://django-compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE
COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_CSS_HASHING_METHOD = 'content'

# Cache everything for 30 minutes
# This only applies to pages that do not have a more specific cache-control
# setting. See urls.py
CACHE_CONTROL_MAX_AGE = 30 * 60


# Configuration from environment variables
# Alternatively, you can set these in a local.py file on the server

env = os.environ.copy()

# On Torchbox servers, many environment variables are prefixed with "CFG_"
for key, value in os.environ.items():
    if key.startswith('CFG_'):
        env[key[4:]] = value


# Basic configuration

APP_NAME = env.get('APP_NAME', 'rca')

if 'SECRET_KEY' in env:
    SECRET_KEY = env['SECRET_KEY']

if 'ALLOWED_HOSTS' in env:
    ALLOWED_HOSTS = env['ALLOWED_HOSTS'].split(',')

if 'PRIMARY_HOST' in env:
    BASE_URL = 'http://%s/' % env['PRIMARY_HOST']

if 'SERVER_EMAIL' in env:
    SERVER_EMAIL = env['SERVER_EMAIL']

if 'CACHE_PURGE_URL' in env:
    INSTALLED_APPS += ('wagtail.contrib.wagtailfrontendcache', )  # noqa
    WAGTAILFRONTENDCACHE = {
        'default': {
            'BACKEND': 'wagtail.contrib.wagtailfrontendcache.backends.HTTPBackend',
            'LOCATION': env['CACHE_PURGE_URL'],
        },
    }

if 'STATIC_URL' in env:
    STATIC_URL = env['STATIC_URL']

if 'STATIC_DIR' in env:
    STATIC_ROOT = env['STATIC_DIR']

if 'MEDIA_URL' in env:
    MEDIA_URL = env['MEDIA_URL']

if 'MEDIA_DIR' in env:
    MEDIA_ROOT = env['MEDIA_DIR']


# Database

if 'DATABASE_URL' in os.environ:
    DATABASES = {'default': dj_database_url.config()}

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env.get('PGDATABASE', APP_NAME),
            'CONN_MAX_AGE': 600,  # number of seconds database connections should persist for

            # User, host and port can be configured by the PGUSER, PGHOST and
            # PGPORT environment variables (these get picked up by libpq).
        }
    }


# Redis
# Redis location can either be passed through with REDIS_HOST or REDIS_SOCKET

if 'REDIS_URL' in env:
    REDIS_LOCATION = env['REDIS_URL']
    BROKER_URL = env['REDIS_URL']

elif 'REDIS_HOST' in env:
    REDIS_LOCATION = env['REDIS_HOST']
    BROKER_URL = 'redis://%s' % env['REDIS_HOST']

elif 'REDIS_SOCKET' in env:
    REDIS_LOCATION = 'unix://%s' % env['REDIS_SOCKET']
    BROKER_URL = 'redis+socket://%s' % env['REDIS_SOCKET']

else:
    REDIS_LOCATION = None


if REDIS_LOCATION is not None:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_LOCATION,
            'KEY_PREFIX': APP_NAME,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }


# Elasticsearch

if 'ELASTICSEARCH_URL' in env:
    WAGTAILSEARCH_BACKENDS = {
        'default': {
            'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch.ElasticSearch',
            'URLS': [env['ELASTICSEARCH_URL']],
            'INDEX': APP_NAME,
            'ATOMIC_REBUILD': True,
        },
    }


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'formatters': {
        'default': {
            'verbose': '[%(asctime)s] (%(process)d/%(thread)d) %(name)s %(levelname)s: %(message)s'
        }
    },
    'loggers': {
        'rca': {
            'handlers': [],
            'level': 'INFO',
            'propagate': False,
            'formatter': 'verbose',
        },
        'wagtail': {
            'handlers': [],
            'level': 'INFO',
            'propagate': False,
            'formatter': 'verbose',
        },
        'compressor': {
            'handlers': [],
            'level': 'INFO',
            'propagate': False,
            'formatter': 'verbose',
        },
        'django': {
            'handlers': [],
            'level': 'INFO',
            'propagate': False,
            'formatter': 'verbose',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
            'formatter': 'verbose',
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
            'formatter': 'verbose',
        },
    },
}


if 'LOG_DIR' in env:
    # {{ cookiecutter.project_name }} log
    LOGGING['handlers']['rca_file'] = {
        'level': 'INFO',
        'class': 'cloghandler.ConcurrentRotatingFileHandler',
        'filename': os.path.join(env['LOG_DIR'], 'rca.log'),
        'maxBytes': 5242880,  # 5MB
        'backupCount': 5
    }
    LOGGING['loggers']['rca']['handlers'].append('rca_file')

    # Wagtail log
    LOGGING['handlers']['wagtail_file'] = {
        'level': 'INFO',
        'class': 'cloghandler.ConcurrentRotatingFileHandler',
        'filename': os.path.join(env['LOG_DIR'], 'wagtail.log'),
        'maxBytes': 5242880,  # 5MB
        'backupCount': 5
    }
    LOGGING['loggers']['wagtail']['handlers'].append('wagtail_file')

    # Error log
    LOGGING['handlers']['errors_file'] = {
        'level': 'ERROR',
        'class': 'cloghandler.ConcurrentRotatingFileHandler',
        'filename': os.path.join(env['LOG_DIR'], 'error.log'),
        'maxBytes': 5242880,  # 5MB
        'backupCount': 5
    }
    LOGGING['loggers']['compressor']['handlers'].append('errors_file')
    LOGGING['loggers']['django']['handlers'].append('errors_file')
    LOGGING['loggers']['django.request']['handlers'].append('errors_file')
    LOGGING['loggers']['django.security']['handlers'].append('errors_file')


try:
    from .local import *  # noqa
except ImportError:
    pass


# Raven (sentry error logging)

# This must be after the .local import as RAVEN_DSN is set in local.py
if 'RAVEN_DSN' in os.environ:
    RAVEN_CONFIG = {
        'dsn': os.environ['RAVEN_DSN'],
        'release': raven.fetch_git_sha(os.path.dirname(os.path.abspath(PROJECT_ROOT))),
    }
