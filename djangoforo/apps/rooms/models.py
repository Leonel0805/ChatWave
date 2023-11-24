from django.db import models
from apps.users.models import User 


    
class Room(models.Model):
    user_host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    likes = models.ManyToManyField(User, related_name='liked_rooms', default=None, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def num_likes(self):
        return self.likes.all().count()

class Like(models.Model):
    
    LIKE_CHOICES = {
        ('Like', 'like'),
        ('Unlike', 'unlike')
    }
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    
    

