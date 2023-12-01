from django.urls import path 
from .apiviews import (RoomListAPIView,
    RoomCreateAPIView,
    LikeRoomListAPIView,
    MyRoomsListAPIView,
    MyRoomEditAPIView,
    RoomSearchAPIView
)

urlpatterns = [
    path('list/', RoomListAPIView.as_view(), name='list-rooms'),
    path('my-list/', MyRoomsListAPIView.as_view(), name='my-list-rooms'),
    path('my-list/<int:pk>/', MyRoomEditAPIView.as_view(), name='my-list-rooms-edit'),
    
    path('search/', RoomSearchAPIView.as_view(), name='room-search'),
    
    
    
    path('list/liked_rooms/', LikeRoomListAPIView.as_view(), name='like-rooms'),
    
    path('create/', RoomCreateAPIView.as_view(), name='create-rooms'),
    
]