from django.urls import path 
from apps.rooms import views 



urlpatterns = [
    path('room_chat/create/', views.room_create, name='room-create' ),
    
    path('room_chat/<int:pk>/', views.room_chat, name='room-chat' ),
]