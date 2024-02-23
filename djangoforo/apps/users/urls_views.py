from django.urls import path
from apps.users.views import me_perfil, me_perfil_edit, user_view, me_perfil_change_password

urlpatterns = [
    
    # Me-Perfil
    path('me-perfil/', me_perfil, name='me-perfil'),
    path('me-perfil/edit/', me_perfil_edit, name='me-perfil-edit'),
    path('me-perfil/edit/change-password/', me_perfil_change_password, name='me-perfil-edit-password'),
    
    
    # Perfil view
    path('user-view/<int:pk>/', user_view, name='user_view' )
    
]
    
    
