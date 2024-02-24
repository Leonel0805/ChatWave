from rest_framework.viewsets import GenericViewSet, ModelViewSet, mixins
from .serializers import (
    UserListSerializer,
    UserSerializer,
    UpdatePasswordSerializer,
    UserViewSerializer
)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
#la diferencia entre GenericViewSet y un ModelViewSet es que el
#model ya tiene los metodos predeterminados y podes sobreescribir
# en cambio GenericViewSet no tiene los metodos

from rest_framework.mixins import UpdateModelMixin

class UserGenericViewSet(GenericViewSet, mixins.UpdateModelMixin):
    
    permission_classes = [AllowAny]

    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer
    queryset = None
    
    #get_object() nos devuelve el objeto por pk
    def get_object(self, pk):
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()

    def get_queryset(self):
 
        if self.queryset is None:
            queryset = self.serializer_class().Meta.model.objects\
                .filter(is_active=True).exclude(username=self.request.user.username)
     
            self.queryset = queryset

        return self.queryset
        
    
    def list(self, request):
        users = self.get_queryset()
        
        print('request.user desde apiview',request.user)
        users_serializer = self.list_serializer_class(users, many=True)
        return Response(users_serializer.data)
    
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
        
        self.serializer_class = UserViewSerializer 
        user = self.get_object(pk)
        
        if user:
            user_serializer = self.serializer_class(user)
            return Response({
                'user':user_serializer.data
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
