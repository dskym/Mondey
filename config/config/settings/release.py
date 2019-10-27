from .base import *

DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES_CONFIG = os.path.join(BASE_DIR, 'config/settings/db_release.cnf')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': DATABASES_CONFIG,
        }
    }
}
