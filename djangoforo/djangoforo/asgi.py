
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoforo.settings.local')

print("Configuración de ASGI en progreso...") 

application = get_asgi_application()
