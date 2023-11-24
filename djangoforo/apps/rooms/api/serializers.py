from rest_framework import serializers
from apps.rooms.models import Room, Like
from apps.users.models import User

class UserRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'email')

class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'user_host', 'name', 'likes')
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        user_id = data['user_host']
        
        user = User.objects.filter(id=user_id).first()
        
        user_serializer = UserRoomSerializer(user)
        
        data['user_host'] = user_serializer.data
        return data

class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('user_host', 'name', 'likes')


class LikeRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user', 'room', 'value')
        