from django.db import models
from  djangoforo.settings.base import AUTH_USER_MODEL

class Room(models.Model):
    user_host = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rooms')
    users_online = models.ManyToManyField(AUTH_USER_MODEL)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='rooms', default='/load/room_chat_logo.jpg' , blank=True, verbose_name='Portada')
    likes = models.ManyToManyField(AUTH_USER_MODEL, related_name='liked_rooms', default=None, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    @property
    def num_likes(self):
        return self.likes.all().count()
    
    def __str__(self):
        return self.name

class Like(models.Model):
    
    LIKE_CHOICES = {
        ('Like', 'like'),
        ('Unlike', 'unlike')
    }
    
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Room: {self.room.name} | User: {self.user}"
    
    
class Message(models.Model):
    
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='messages', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    

