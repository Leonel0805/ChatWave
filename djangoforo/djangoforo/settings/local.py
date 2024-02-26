from .base import *


DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '6d30-2800-810-507-a12f-19e-5994-8b3a-e823.ngrok-free.app']

#config ngrok csrf
# CSRF_TRUSTED_ORIGINS = ['https://6d30-2800-810-507-a12f-19e-5994-8b3a-e823.ngrok-free.app']


#database local
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

