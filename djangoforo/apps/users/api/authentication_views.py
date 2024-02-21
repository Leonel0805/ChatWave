from django.contrib.auth import authenticate

from apps.users.models import User 
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import(
    UserSerializer,
    UserMeSerializer
)


#Registro de ususarios, no proveemos un token, solo en el login
class UserRegisterAPIView(APIView):

    def post(self, request):
        
        # serializamo lo obtenido por POST
        user_serializer = UserSerializer(data = request.data)
        
        if user_serializer.is_valid():
            user = user_serializer.save()
            
            return Response({
                'message': 'User created successfully'
            }, status=status.HTTP_201_CREATED)
            
        else:
            return Response({
                'error': user_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
class UserLoginAPIView(APIView):
     
    serializer_class = TokenObtainPairSerializer
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
          
        # authenticate recibe username y password
        user_authenticate = authenticate(
            username=email,
            password=password
        )
        
        #buscamos el mail en caso de existir, si existe estan mal las credenciales
        email_found = User.objects.filter(email=email).first() 
        
        if user_authenticate:
            login_serializer = self.serializer_class(data = request.data)
            if login_serializer.is_valid():
                user_serializer = UserMeSerializer(user_authenticate)
                
                return Response({
                    'token': login_serializer.validated_data['access'],
                    'refresh': login_serializer.validated_data['refresh'],
                    'user': user_serializer.data,
                    'message':"Login successfully!"
                }, status=status.HTTP_200_OK)
                

        elif email_found: 
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
            
            
#Logout
class UserLogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = TokenObtainPairSerializer()
    
    def post(self, request):

        user = User.objects.filter(pk = request.user.id).first()

        if user:
            RefreshToken.for_user(user)
            return Response({
                'message':'Logout successfully!'
            })
        
   
        return Response({
            'error': 'Not found'
        })