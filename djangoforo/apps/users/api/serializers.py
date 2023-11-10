from rest_framework import serializers
from apps.users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'email', 'username', 'bio', 'avatar', 'password')
        
class TokenObtainPairSerializer(TokenObtainPairSerializer):
    pass

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('username','email','password')
        
    def create(self, validated_data):
        
        password = validated_data.pop('password')
        print(password)
        
        user = User.objects.create_user(**validated_data, password = password)
        user.save()
        return user
    

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('email', 'username', 'bio', 'avatar')
        
class UpdatePasswordSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(max_length=128)
    
    class Meta:
        model = User 
        fields = ('password', 'password2')
        
    def update(self, instance, validated_data):

        new_password = validated_data.get('password', instance.password)
        
        if new_password == validated_data['password2']:
        
            instance.set_password(new_password)
            instance.save()
            return instance
            
        else:
            raise serializers.ValidationError('Error password')
        
