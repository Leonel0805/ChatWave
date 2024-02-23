from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework.response import Response
from .serializers import UserMeSerializer, UpdatePasswordSerializer

# Apiview get, put, patch
class UserMeAPIView(RetrieveUpdateAPIView):
       
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = UserMeSerializer
    
    def get_object(self):
        return self.request.user


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
         