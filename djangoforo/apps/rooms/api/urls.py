from django.urls import path 
from .apiviews import RoomListAPIView, RoomCreateAPIView

urlpatterns = [
    path('list/', RoomListAPIView.as_view(), name='list-rooms'),
    path('create/', RoomCreateAPIView.as_view(), name='create-rooms'),
    
]