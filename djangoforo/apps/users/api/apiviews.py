from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import UserMeSerializer

class UserMeAPIView(RetrieveUpdateAPIView):
       
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = UserMeSerializer
    
    def get_object(self):
        return self.request.user
