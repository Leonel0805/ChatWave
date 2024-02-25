import json 

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from apps.users.models import User, Profile
from apps.rooms.models import Message, Room
from django.contrib import messages

# from apps.core.views import get_userhost


class ChatConsumer(AsyncWebsocketConsumer):
    
    #nos conectamos
    async def connect(self):
        
        self.room_name = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = f'chat_{self.room_name}'
    
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        self.user = self.scope['user']
        
        await self.accept()
    
        
        
     #nos desconectamos
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    
    
    def get_connected_users(self):
        users = []
        for user in User.objects.filter(profile__is_online=True):
            users.append(user.username)
        return users 
    
    # Enviar la lista de usuarios conectados
    async def send_user_list(self):
    # Obtener la lista de usuarios conectados
        connected_users = await sync_to_async(self.get_connected_users)()
        
        # Enviar la lista de usuarios conectados al cliente
        await self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': connected_users
        }))
        

        
    async def receive(self, text_data):
        
        data = json.loads(text_data)
        if data.get('type') == 'connect_user':
            # Manejar la conexión del usuario
            username = data.get('username')
            print('Usuario conectado:', username)
            
            await self.save_user_connect(username)
            await self.send_user_list()
        
        elif data.get('type') == 'message_chat':
             
            message = data['message']
            
            username = data['username']
            room = data['room'] 
        
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
    
    @database_sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.filter(email=username).first()
        room = Room.objects.filter(pk=room).first()
        print(message)
        Message.objects.create(user=user, room=room, content=message)
    
       # Obtener la lista de usuarios conectados
    @database_sync_to_async
    def save_user_connect(self, username):
        user = User.objects.filter(email=username).first()
        Profile.objects.create(user=user, is_online=True)
