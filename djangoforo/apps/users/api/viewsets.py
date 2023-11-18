from apps.users.models import User 
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from .serializers import (
    UserListSerializer,
    UserSerializer,
    UpdateUserSerializer,
    UpdatePasswordSerializer,
    UserMeSerializer
)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
#la diferencia entre GenericViewSet y un ModelViewSet es que el
#model ya tiene los metodos predeterminados y podes sobreescribir
# en cambio GenericViewSet no tiene los metodos

class UserGenericViewSet(GenericViewSet):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer
    update_serializer_class = UpdateUserSerializer
    queryset = None
    
    #get_object() nos devuelve el objeto por pk
    def get_object(self, pk):
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()
    
    def get_queryset(self):
        
        if self.queryset is None:
            self.queryset = self.serializer_class().Meta.model.objects\
                .filter(is_active=True)
            return self.queryset
        else:
            return self.queryset
    
    
    def list(self, request):
        users = self.get_queryset()
        
        users_serializer = self.list_serializer_class(users, many=True)
        return Response({
            'users':users_serializer.data
        })
    
    def create(self, request):
        user_serializer = UserSerializer(data=request.data)
        
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'user':user_serializer.data
            })
        else:
            return Response({
                'error': 'not valid'
            })
            
    def retrieve(self, request, pk=None):
        
        self.serializer_class = self.update_serializer_class
       # user = User.objects.filter(pk = pk).first()
        user = self.get_object(pk)
        
        if user:
            user_serializer = self.serializer_class(user)
            return Response({
                'user':user_serializer.data
            })
            
    def update(self, request, pk=None):
        
        user = self.get_object(pk)
        
        if user:
            user_serializer = UpdateUserSerializer(user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({
                    'user update': user_serializer.data
                })
    
    @action(detail=True, methods=['put'], url_path='set_password', serializer_class=UpdatePasswordSerializer)
    def set_password(self, request, pk=None):
        user = self.get_object(pk)
        
        if user:
            password_serializer = UpdatePasswordSerializer(user, data=request.data)
            if password_serializer.is_valid():
                password_serializer.save()
                return Response({
                    'message':'password change'
                })    
            
    
        return Response({
            'error': 'not found'
        })
            
    def destroy(self, request, pk=None):
        user = self.get_object(pk)
        
        if user:
            user.is_active = False
            user.save()
            return Response({
                'message':'Usuario eliminado!'
            })
    
        return Response({
            'error':'NOT FOUND'
        })

class UserMeAPIView(RetrieveAPIView):
       
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = UserMeSerializer
    
    def get_object(self):
        return self.request.user