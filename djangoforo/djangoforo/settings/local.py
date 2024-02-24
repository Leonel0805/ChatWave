from .base import *


DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.0.10']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL =  '/media/'
MEDIA_ROOT = BASE_DIR / 'static/media'

