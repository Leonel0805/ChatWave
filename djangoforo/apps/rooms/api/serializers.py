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
        fields = ('id', 'user_host', 'name', 'image',  'likes')
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        user_id = data['user_host']  
        user = User.objects.filter(id=user_id).first()
        user_serializer = UserRoomSerializer(user)
        
        data['likes']= instance.num_likes
        data['user_host'] = user_serializer.data
        
        return data
    
class ListMyRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room 
        fields = ('id', 'name', 'description', 'image', 'likes')
        read_only_fields = ('id', 'likes' )
        
    def update(self, instance, validated_data):
        
        image_file = self.context['request'].FILES.get('image', None)

        if not image_file:
            # Si no se proporciona un archivo
            validated_data.pop('image', None)

        #llamamos al update predeterminado padre
        return super().update(instance, validated_data)    
    
    
    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['likes']= instance.num_likes
        
        return data

class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('user_host', 'name','description', 'image', 'likes')
        read_only_fields = ('user_host',)
   
    def validate(self, data):
        user_host = self.context['request'].user
        data['user_host'] = user_host

        return data
    
            
class LikeRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user', 'room', 'value')
        

        