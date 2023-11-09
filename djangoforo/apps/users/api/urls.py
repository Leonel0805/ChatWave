from django.urls import path
from .views import (
    UserListAPIView,
    UserRegisterAPIView,
    UserLoginAPIView,
    UserLogoutAPIView
)


urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='users-list'),
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('logout/', UserLogoutAPIView.as_view(), name='user-logout'),
      

    
]
