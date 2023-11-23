from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from djangoforo.settings.local import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rutas de app
    path('app/', include('apps.core.urls')),
    path('app/', include('apps.users.urls_views')),
    path('app/', include('apps.rooms.urls_views')),
    
    # Rutas de api
    path('api/authentication/', include('apps.users.api.urls')),
    path('api/usersview/', include('apps.users.api.routers')),

    # Rutas de simple_jwt
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
]
if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
