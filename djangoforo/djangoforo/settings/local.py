from .base import *


DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '2b34-2800-810-507-a12f-bd4a-1711-7f4d-cf11.ngrok-free.app']

#config ngrok csrf
# CSRF_TRUSTED_ORIGINS = ['https://2b34-2800-810-507-a12f-bd4a-1711-7f4d-cf11.ngrok-free.app']


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

