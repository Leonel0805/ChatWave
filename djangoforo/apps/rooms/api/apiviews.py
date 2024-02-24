from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .serializers import RoomListSerializer, RoomCreateSerializer, LikeRoomSerializer, ListMyRoomSerializer
from apps.rooms.models import Room
from apps.users.models import User
   
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
        
            
class RoomListAPIView(APIView):
    
   def get(self, request, pk=None):
       
        if pk is not None:
            print('Entramos a user.rooms')
            user = User.objects.filter(id=pk).first()
            if user:
                rooms = user.rooms.all().order_by('-created_at')
                if len(rooms) == 0:
                    
                    return Response({
                        'message': 'No hay rooms creados'
                    }, status=status.HTTP_202_ACCEPTED) # 204
            else:
                return Response({
                    'error': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            print('No entramos')
            rooms = Room.objects.all().order_by('-created_at')
            
        rooms_serializer = RoomListSerializer(rooms, many=True)
        return Response(rooms_serializer.data, status=status.HTTP_200_OK)
    

class RoomSearchAPIView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        query_param = self.request.query_params.get('search', '')
        print(query_param)
        
        if query_param != '':
            rooms = Room.objects.filter(name__icontains = query_param)
            rooms_serializer = RoomListSerializer(rooms, many=True)
        
        else:
            rooms = {}
            rooms_serializer = RoomListSerializer(rooms, many=True)
        
        return Response(rooms_serializer.data)
    
    
class LikeRoomListAPIView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
     
    def get(self, request):
        
        user = request.user
        
        liked_rooms = user.liked_rooms.all()    

        liked_rooms = RoomListSerializer(liked_rooms, many=True)
        return Response(liked_rooms.data)
    
class MyRoomsListAPIView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        user = request.user
        rooms = Room.objects.filter(user_host=user).order_by('-created_at')
    

        rooms_serializer = ListMyRoomSerializer(rooms, many=True)
        return Response(rooms_serializer.data)

class MyRoomEditAPIView(RetrieveUpdateDestroyAPIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = ListMyRoomSerializer
    
    def get_queryset(self):
        return Room.objects.filter(user_host=self.request.user)

        
