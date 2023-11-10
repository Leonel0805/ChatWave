from apps.users.models import User 
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .serializers import UserListSerializer, UserSerializer, UpdateUserSerializer

from rest_framework.decorators import action
from rest_framework.response import Response

#la diferencia entre GenericViewSet y un ModelViewSet es que el
#model ya tiene los metodos predeterminados y podes sobreescribir
# en cambio GenericViewSet no tiene los metodos

class UserGenericViewSet(GenericViewSet):
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
        
       # user = User.objects.filter(pk = pk).first()
        user = self.get_object(pk)
        
        if user:
            user_serializer = self.list_serializer_class(user)
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
    
    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        pass
    
    def destroy(self, request, pk=None):
        user = self.get_object(pk)
        
        if user:
            user.is_active = False
            user.save()
            return Response({
                'message':'Usuario eliminado!'
            })
        else:
            return Response({
                'error':'NOT FOUND'
            })
#Model view set
class UsersViewSet(ModelViewSet):
    serializer_class = UserListSerializer
    queryset = User.objects.all()