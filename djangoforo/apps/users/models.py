from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

from apps.rooms.models import Room
# Custom User Manager
class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, username, password = None, **extra_fields):
        if not email:
            raise ValueError('Email not provided')
        
        email = self.normalize_email(email)
        
        #Creamos el usuario
        user = self.model(
            email = email,
            username = username
        )
    
        #seteamos la password    
        user.set_password(password)
        user.save()
        
        return user 
    
    def create_superuser(self, email, username, password=None, **extra_fields):
       # extra_fields.setdefault('is_staff', True)
        #extra_fields.setdefault('is_superuser', True)
        
        user = self.create_user(email, username, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        return user 

# Custom User, sin First_name o Last_name que debe contener AbstrasUser
class User(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(max_length=25, unique=True, blank=False)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='img/user', default='/load/foto_perfil.jpg', blank=True, null=True, verbose_name='Imagenlol')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_join = models.DateTimeField(default=timezone.now)
    
    objects = CustomUserManager()
    
    # indicamos por que metodo vamos a iniciar sesion, por ejemplo admin de django
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    
    REQUIRED_FIELDS = ['username']
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_online = models.BooleanField(default=False)
    
    def __str__(self):
        return f"User: {self.user} - Online: {self.is_online}"
    
    
class CustomToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"User: {self.user} - Token: {self.token}"
    