import json 

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from apps.users.models import User 
from apps.rooms.models import Message, Room
from django.contrib import messages

# from apps.core.views import get_userhost

def get_userhost(request):
    user_host_jsonstr = request.COOKIES.get('User')
    
    if user_host_jsonstr is not None:
        #convertimos el userstr en objeto dict 
        user_host = json.loads(user_host_jsonstr)
        return user_host


class ChatConsumer(AsyncWebsocketConsumer):
    
    #nos conectamos
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = f'chat_{self.room_name}'
        
    
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        
        
     #nos desconectamos
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        message = data['message']
        
        username = data['username']
        room = data['room'] 
        
        
        print(username)
        print(message_type)
        await self.save_message(username, room, message)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'message_chat',
                'message':message,
                'username':username
            }
             
        )   
        
    async def message_chat(self, event):
        message = event['message']
        username = event['username']
    
        await self.send(text_data=json.dumps({
            'message':message,
            'username':username
        })
        )
    
    @sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.filter(email=username).first()
        room = Room.objects.filter(pk=room).first()
        print(message)
        Message.objects.create(user=user, room=room, content=message)
    
    
