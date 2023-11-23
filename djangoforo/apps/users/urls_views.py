from django.urls import path
from apps.users.views import me_perfil, me_perfil_edit, user_view

urlpatterns = [
    
    # Me-Perfil
    path('me_perfil/', me_perfil, name='me-perfil'),
    path('me_perfil_edit/', me_perfil_edit, name='me-perfil-edit'),
    
    # Perfil view
    path('user_view/<int:pk>/', user_view, name='user_view' )
    
]
    
    
