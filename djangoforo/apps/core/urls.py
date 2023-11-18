from django.urls import path
from . import views
from apps.users.views import me_perfil

urlpatterns = [
    path('home/', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    path('me_perfil/', me_perfil, name='me-perfil'),
    
    
]
