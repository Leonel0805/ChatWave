from rest_framework import serializers
from apps.users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('email', 'username', 'bio', 'avatar')
        
class TokenObtainPairSerializer(TokenObtainPairSerializer):
    pass

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('username','email','password')
        
        
    def create(self, validate_data):
        
        password = validate_data.pop('password')
        print(password)
        
        user = User.objects.create_user(**validate_data, password = password)
        user.save()
        return user