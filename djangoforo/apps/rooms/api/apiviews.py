from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .serializers import RoomListSerializer, RoomCreateSerializer, LikeRoomSerializer, ListMyRoomSerializer
from apps.rooms.models import Room

class RoomListAPIView(APIView):
    
    def get(self, request):
        
        rooms = Room.objects.all().order_by('-created_at')
        
        rooms_serializer = RoomListSerializer(rooms, many=True)
        return Response(rooms_serializer.data)
    
    
class MyRoomsListAPIView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        user = request.user
        rooms = Room.objects.filter(user_host=user).order_by('-created_at')
    
        print(rooms)

        rooms_serializer = ListMyRoomSerializer(rooms, many=True)
        return Response(rooms_serializer.data)

class MyRoomEditAPIView(RetrieveUpdateDestroyAPIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = ListMyRoomSerializer
    
    def get_queryset(self):
        return Room.objects.filter(user_host=self.request.user)

        
        
class LikeRoomListAPIView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
     
    def get(self, request):
        
        user = request.user
        
        liked_rooms = user.liked_rooms.all()    

        liked_rooms = RoomListSerializer(liked_rooms, many=True)
        return Response(liked_rooms.data)
        
    
class RoomCreateAPIView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
     
    def post(self, request):
        room_serializer =  RoomCreateSerializer(data=request.data, context={'request':request} )
        print(room_serializer)
        if room_serializer.is_valid():
            room_serializer.save()
            
            return Response({
                'message':'Room created!!'
            }, status=status.HTTP_201_CREATED)
            
        else:
            return Response({
                'error':'Not created',
                'details':room_serializer.errors
            },status=status.HTTP_400_BAD_REQUEST)
        
            