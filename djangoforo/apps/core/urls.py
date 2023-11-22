from django.urls import path
from . import views
from apps.users.views import me_perfil, me_perfil_edit

urlpatterns = [
    path('home/', views.home, name='home'),
    path('index/', views.index, name='index'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    # Me-Perfil
    path('me_perfil/', me_perfil, name='me-perfil'),
    path('me_perfil_edit/', me_perfil_edit, name='me-perfil-edit'),
    
    
    
]
