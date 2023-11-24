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
    
    
    @action(detail=True, methods=['patch'],  url_path='like-room', serializer_class=LikeRoomSerializer)
    def like_unlike_room(self, request, pk):
        
        room = Room.objects.filter(id=pk).first()
 
        if room:
            request.data['user'] = request.user.id
            request.data['room'] = room.pk
        
            
            print(request.data)
            like_serializer = LikeRoomSerializer(data=request.data)
        
            if like_serializer.is_valid():
                like_object = Like.objects.filter(user=request.data['user'], room=request.data['room']).first()
                
                if like_object:    
                    like_object.delete()
                    return Response({
                        'message':'Room Unliked!'
                    })

                else:
                    like_serializer.save()
                    return Response({
                        'message':'Room liked!'
                    })
            
         
        
        return Response({
            'error':'error'
        })
                
        