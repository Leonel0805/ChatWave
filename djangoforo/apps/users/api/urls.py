from django.urls import path
from .authentication_views import (
    UserRegisterAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,

)

from .apiviews import (
    UserMeAPIView,
    UserMeChangePasswordAPIView
)


urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('logout/', UserLogoutAPIView.as_view(), name='user-logout'),
    path('me/', UserMeAPIView.as_view(), name='user-me'),
    path('me/change-password/', UserMeChangePasswordAPIView.as_view(), name='user-me-change-password'),
         
]
