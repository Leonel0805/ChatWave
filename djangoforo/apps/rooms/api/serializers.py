from rest_framework import serializers
from apps.rooms.models import Room, Like

class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'user_host', 'name', 'likes')
        

class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('user_host', 'name', 'likes')


class LikeRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user', 'room', 'value')
        