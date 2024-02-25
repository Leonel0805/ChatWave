from django.urls import path 
from . import consumers

websocket_urlpatterns = [
    path('ws/<int:pk>/', consumers.ChatConsumer.as_asgi()),
    path('ws/users_online/', consumers.UserOnline.as_asgi()),
    
]