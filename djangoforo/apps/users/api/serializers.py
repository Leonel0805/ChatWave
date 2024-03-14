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
        fields = ('username','email', 'avatar', 'password')
        
    def create(self, validated_data):
        
        password = validated_data.pop('password')
        # print(password)
        user = User.objects.create_user(**validated_data, password = password)
        user.save()
        return user

class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'email', 'username', 'bio', 'avatar')
        
    def update(self, instance, validated_data):
        
        avatar_file = self.context['request'].FILES.get('avatar', None)

        if not avatar_file:
            # Si no se proporciona un archivo 'avatar'
            validated_data.pop('avatar', None)

        #llamamos al update predeterminado padre
        return super().update(instance, validated_data)
        
        
class UpdatePasswordSerializer(serializers.ModelSerializer):
    
    new_password = serializers.CharField(max_length=128)
    
    class Meta:
        model = User 
        fields = ('password', 'new_password')
        
    def update(self, instance, validated_data):
        new_password = validated_data.get('new_password')
        password = validated_data.get('password')

        if not instance.check_password(password):
            raise serializers.ValidationError('La contraseña actual es incorrecta.')
        
        if new_password == password:
            raise serializers.ValidationError('La nueva contraseña no puede ser igual a la contraseña actual.')
        

        instance.set_password(new_password)
        instance.save()
        
        return instance
    
    
class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('username','email', 'bio', 'avatar')
            

        
