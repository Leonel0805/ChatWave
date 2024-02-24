from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.users.models import User
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserMeSerializer, UpdatePasswordSerializer, UserListSerializer

# Apiview get, put, patch
class UserMeAPIView(RetrieveUpdateAPIView):
       
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = UserMeSerializer
    
    def get_object(self):
        return self.request.user

class UserListAPIView(ListAPIView):
           
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    
    serializer_class = UserListSerializer
    
    def get_queryset(self):
        queryset = User.objects.all()
        
        if self.request.user.is_authenticated:
            queryset = User.objects.all().exclude(email=self.request.user.email)
        return queryset
    
    

# APIView Cambiar contraseña
class UserMeChangePasswordAPIView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        user = request.user
        if user:
            password_serializer = UpdatePasswordSerializer(user, data=request.data)
            if password_serializer.is_valid():
                password_serializer.save()
                return Response({
                    'message':'Contraseña cambiada'
                }, status=status.HTTP_200_OK)    
            
            else:
              
                return Response({
                    'error': password_serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
         