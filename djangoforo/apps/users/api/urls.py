from django.urls import path
from .authentication_views import (
    UserRegisterAPIView,
    UserLoginAPIView,
    UserLogoutAPIView
)


urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('logout/', UserLogoutAPIView.as_view(), name='user-logout'),
      
]
