from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import RoomListSerializer, RoomCreateSerializer, LikeRoomSerializer
from apps.rooms.models import Room

class RoomListAPIView(APIView):
    
    def get(self, request):
        
        rooms = Room.objects.all()
        
        rooms_serializer = RoomListSerializer(rooms, many=True)
        return Response({
            'rooms': rooms_serializer.data
        })
        
        
class RoomCreateAPIView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
     
    def post(self, request):
        
        request.data['user_host'] = request.user.pk
        
        room_serializer =  RoomCreateSerializer(data=request.data)
        
        if room_serializer.is_valid():
            room_serializer.save()
            
            return Response({
                'message':'Room created!!'
            })
            
        else:
            return Response({
                'error':'Not created'
            })
        
            