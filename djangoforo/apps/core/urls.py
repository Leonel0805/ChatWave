from django.urls import path
from . import views
from apps.users.views import me_perfil, me_perfil_edit, user_view

urlpatterns = [
    path('home/', views.home, name='home'),
    path('search/', views.search, name='search'),
    
    path('index/', views.index, name='index'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
 
    
]
