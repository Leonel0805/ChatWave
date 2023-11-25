from rest_framework.viewsets import GenericViewSet
from .serializers import RoomListSerializer, LikeRoomSerializer
from apps.rooms.models import Room, Like
from rest_framework.response import Response

from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class RoomGenericViewSet(GenericViewSet):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = RoomListSerializer
    
    def get_object(self, pk):
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()
    
    def retrieve(self, request, pk):
        room = self.get_object(pk)
        
        if room:
            room_serializer = self.serializer_class(room)
            return Response({
                'room':room_serializer.data
            })
        
        else:
            return Response({
                'error': 'Not found'
            })
    
    
    @action(detail=True, methods=['post'],  url_path='like-room', serializer_class=LikeRoomSerializer)
    def like_room(self, request, pk=None, value='Like'):
        return self.like_unlike_room(request, pk, value)
    
    @action(detail=True, methods=['post'],  url_path='unlike-room', serializer_class=LikeRoomSerializer)
    def unlike_room(self, request, pk=None, value='Unlike'):
        return self.like_unlike_room(request, pk, value)

        
    def like_unlike_room(self, request, pk, value):
        
        room = Room.objects.filter(id=pk).first()
        user = request.user

        if room:
            request.data['user'] = user.id
            request.data['room'] = room.pk
            request.data['value'] = value
            
            print(request.data)
            like_serializer = LikeRoomSerializer(data=request.data)
        
            if like_serializer.is_valid():
                like = like_serializer.save()
                
                if like.value == 'Like':
                    user.liked_rooms.add(room)
                    return Response({
                        'message':'Room liked!'
                    })
                
                else:
                    user.liked_rooms.remove(room)
                    return Response({
                        'message':'Unlike Room!'
                    })
        
        return Response({
            'error':like_serializer.errors
        })
        