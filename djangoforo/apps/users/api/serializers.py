from rest_framework import serializers
from apps.users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'email', 'username', 'bio', 'avatar')
        
class TokenObtainPairSerializer(TokenObtainPairSerializer):
    pass

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('username','email','password')
        
    def create(self, validate_data):
        
        password = validate_data.pop('password')
        print(password)
        
        user = User.objects.create_user(**validate_data, password = password)
        user.save()
        return user
    

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('username', 'email')