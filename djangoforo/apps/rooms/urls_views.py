from django.urls import path 
from apps.rooms import views 



urlpatterns = [
    path('room_chat/create/', views.room_create, name='room-create' ),
    
    path('room_chat/<int:pk>/', views.room_chat, name='room-chat' ),
    path('room_chat/<int:pk>/like/', views.room_like, name='room-like' ),
    path('room_chat/<int:pk>/delete/', views.room_delete, name='room-delete' ),
    
    
]