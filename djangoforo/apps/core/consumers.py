import json 
from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from apps.users.models import User, Profile, CustomToken
from apps.rooms.models import Message, Room


# from apps.core.views import get_userhost

async def get_token_url(chatconsumer):        
    cookies = chatconsumer.scope['cookies']
    token = cookies.get('Bearer')

    return token

@database_sync_to_async
def get_user_authenticated(token):
    custom_token = CustomToken.objects.filter(token=token).first()
    authenticated_user = custom_token.user
    return authenticated_user
        
async def user_tojson(connected_users):
        
    users_serializer = []
    for user in connected_users:      
        users_serializer.append({
            'username': user.username,  
        })
        
    return users_serializer
    

class ChatConsumer(AsyncWebsocketConsumer):

    #nos conectamos
    async def connect(self):
        
        self.room_id = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = f'chat_{self.room_id}'
    
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        token = await get_token_url(self)
        
        if token:
            authenticated_user = await get_user_authenticated(token)
            await self.save_user_connect_room(authenticated_user, self.room_id)
            await self.send_user_list(self.room_id)

        else:   
            print("No token")
        
        
     #nos desconectamos
    async def disconnect(self, code):

        print('desconexion de websocket room desde servidor')
        token = await get_token_url(self)
        if token:
            authenticated_user = await get_user_authenticated(token)
            await self.remove_user_online(authenticated_user, self.room_id)
            await self.send_user_list(self.room_id)      
            
        else:
            print('No token')
            
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
          
    async def receive(self, text_data):
        
        data = json.loads(text_data)
        
        if data.get('type') == 'message_chat':
             
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
            'type':event['type'],
            'message':message,
            'username':username
        })
        )
        
    
    async def send_user_list(self, room_id):
        # Obtener la lista de usuarios conectados
        connected_users = await self.get_room_users_online(room_id)
        
        connected_users_serializer = await user_tojson(connected_users)
        
        users_online = {
            'connected_users': connected_users_serializer
        }
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_list_room_connect',
                'message': users_online
            },
        )

    async def user_list_room_connect(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message']
        }))
 
    
    @database_sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.filter(email=username).first()
        room = Room.objects.filter(pk=room).first()
        print(message)
        Message.objects.create(user=user, room=room, content=message)
    
    @database_sync_to_async
    def get_room_users_online(self, room_id):
        room = Room.objects.filter(pk=room_id).first()
        if room:
            users = room.users_online.all()
            return list(users)    

       # Guardamos el user dentro de users_online de la room
    @database_sync_to_async
    def save_user_connect_room(self, user_authenticated, room_id):    
        room = Room.objects.filter(pk=room_id).first()
        room.users_online.add(user_authenticated)
        
        #Eliminamos el user dentro de users_online de la room
    @database_sync_to_async
    def remove_user_online(self, user_authenticated, room_id):
        room = Room.objects.filter(pk=room_id).first()
        room.users_online.remove(user_authenticated)

  
# connected_users = set()
class UserOnline(AsyncWebsocketConsumer):
    async def connect(self):

        await self.accept()
        
        #Agregamos el usuario al group del websocket
        await self.channel_layer.group_add("chat_group", self.channel_name)
        
        token = await get_token_url(self)
        if token:
            # Agregar usuario a de usuarios conectados, set is_online=True 
            await self.connect_user(token)
            await self.send_users_online_to_group()

        # Enviar lista de usuarios conectados a todos en el grupo


    async def disconnect(self, close_code):
        
        token = await get_token_url(self)
        
        if token:
            await self.disconnect_user(token)
            await self.send_users_online_to_group()

        await self.channel_layer.group_discard("chat_group", self.channel_name)
    

    async def receive(self, text_data):
       
        # pass
        await self.send_users_online_to_group()
 
 
 
    #Enviamos la lista de usuarios online a todo el group del websocket 
    async def send_users_online_to_group(self):
        
        connected_users = await self.get_users_online()
        connected_users_serializer = await user_tojson(connected_users)
        
        users_online = {
            'connected_users': connected_users_serializer
        }
        await self.channel_layer.group_send(
            "chat_group",
            {
                'type': 'user_list_connect',
                'message': users_online
            },
        )

    async def user_list_connect(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message']
        }))
 
    #CONSULTAS DATABASE
    
    #Obtenemos todos los usuarios is_online=True
    @database_sync_to_async
    def get_users_online(self):
        profiles = Profile.objects.filter(is_online=True)
        
        users = []
        for profile in profiles:
            users.append(profile.user)
        
        return list(users)
    
    #Conectamos usuario create, set is_online=True
    @database_sync_to_async
    def connect_user(self, token):
        custom_token = CustomToken.objects.filter(token=token).first()
        authenticated_user = custom_token.user
            
        profile = Profile.objects.filter(user=authenticated_user).first()
        
        if not profile:
            Profile.objects.create(user=authenticated_user, is_online=True)
        
        else:
            profile.is_online = True
            profile.save()
            
                 
    #Set el usuario is_online=False
    @database_sync_to_async
    def disconnect_user(self, token):
        custom_token = CustomToken.objects.filter(token=token).first()
        authenticated_user = custom_token.user
        user_online = Profile.objects.filter(user=authenticated_user).first()
        user_online.is_online = False
        user_online.save()
        

    

        
        
