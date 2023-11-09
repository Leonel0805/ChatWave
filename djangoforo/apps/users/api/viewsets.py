from apps.users.models import User 
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .serializers import UserSerializer, UserRegisterSerializer

from rest_framework.response import Response

#la diferencia entre GenericViewSet y un ModelViewSet es que el
#model ya tiene los metodos predeterminados y podes sobreescribir
# en cambio GenericViewSet no tiene los metodos

class UserGenericViewSet(GenericViewSet):
    serializer_class = UserSerializer
    
    def get_queryset(self):
        self.queryset = self.serializer_class().Meta.model.objects\
            .filter(is_active=True)
        return self.queryset
    
    
    def list(self, request):
        users = self.get_queryset()
        
        users_serializer = self.serializer_class(users, many=True)
        return Response({
            'users':users_serializer.data
        })
    
    def create(self, request):
        user_serializer = UserRegisterSerializer(data=request.data)
        
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'user':user_serializer.data
            })
        else:
            return Response({
                'error': 'not valid'
            })
            
class UsersViewSet(ModelViewSet):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()