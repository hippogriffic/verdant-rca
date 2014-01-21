from .base import *

DEBUG = False

ALLOWED_HOSTS = ['rca-staging.torchboxapps.com', 'verdant-rca-staging.torchboxapps.com', 'verdant-rca-production.torchboxapps.com', 'www.rca.ac.uk']

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

DEFAULT_FROM_EMAIL = 'publications@rca.ac.uk'

# BASE_URL required for notification emails
BASE_URL = 'http://rca-staging.torchboxapps.com'

# LDAP
from rca_ldap.settings import *

AUTH_LDAP_BIND_DN = ''
AUTH_LDAP_BIND_PASSWORD = ''
AUTH_LDAP_SERVER_URI = 'ldaps://194.80.196.3:636'

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)


try:
	from .local import *
except ImportError:
	pass
