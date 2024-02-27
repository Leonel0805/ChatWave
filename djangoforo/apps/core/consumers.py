import json 
from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from apps.users.models import User, Profile, CustomToken
from apps.rooms.models import Message, Room


# from apps.core.views import get_userhost

async def get_token_url(chatconsumer):        
    query_string = chatconsumer.scope.get('query_string', b'').decode('utf-8')
    query_params = parse_qs(query_string)

    # Obtener el token de autorización de los parámetros de consulta
    token = query_params.get('Authorization', [''])[0]

    return token

        
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
        # Procesar el token si es necesario
        if token:
            print("Token:", token)
            # Realiza acciones con el token, como validación, almacenamiento, etc.
        else:
            print("No token")
        
        
     #nos desconectamos
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        print('desconexion de websocket desde servidor')
        token = await get_token_url(self)
        if token:
            room_id = self.room_id
            await self.remove_user_online(token, room_id)
            print('user removido')
            
        else:
            print('No token')
        

    async def send_user_list(self, room_id):
        # Obtener la lista de usuarios conectados
        connected_users = await self.get_room_users_online(room_id)
        
        # Serializar toda la lista de usuarios conectados
        users_serializer = await user_tojson(connected_users)
        
 
        # Enviar la lista de usuarios conectados al cliente
        await self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': users_serializer
        }))


        
    async def receive(self, text_data):
        
        data = json.loads(text_data)
        if data.get('type') == 'connect_user':
            # Manejar la conexión del usuario
            username = data.get('username')
            room_id = data.get('room')
            
            await self.save_user_connect_room(username, room_id)
            await self.send_user_list(room_id)
            
        
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
    
    @database_sync_to_async
    def get_room_users_online(self, room_id):
        # Supongamos que Room y User son modelos de SQLAlchemy
        # Debes ajustar esto según cómo esté estructurada tu base de datos y modelo de datos
        room = Room.objects.filter(pk=room_id).first()
        if room:
            users = room.users_online.all()
            return list(users)    

       # Guardamos el user dentro de users_online de la room
    @database_sync_to_async
    def save_user_connect_room(self, username, room_id):
        user = User.objects.filter(email=username).first()
        room = Room.objects.filter(pk=room_id).first()
        
        # Agregamos al Room nuestro user en users_online
        print('llegamos a user_conenect')
        room.users_online.add(user)
        
        
    @database_sync_to_async
    def remove_user_online(self, token, room_id):
        customtoken = CustomToken.objects.filter(token=token).first()
        user = customtoken.user
        room = Room.objects.filter(pk=room_id).first()
        room.users_online.remove(user)

  
class UserOnline(AsyncWebsocketConsumer):
    async def connect(self):

        await self.accept()
    

    async def disconnect(self, close_code):
        
        print('desconexion')
        
        cookies = self.scope['cookies']
        token = cookies.get('Bearer')
        print('cookie desconectado', token)
        
        if token:
            await self.disconnect_user(token)
            print('usuario desconectado enviando lista')
            users_online = await self.get_users_online()
            users_serializer = await user_tojson(users_online)
            await self.send(text_data=json.dumps({
                'type': 'user_list_disconnect',
                'users': users_serializer
            }))
            
            print('mensaje disconnect enviado')

            
        else:
            print("No token")
        

        

    async def receive(self, text_data):
    
    
        cookies = self.scope['cookies']
        token = cookies.get('Bearer')
        print('cookie', token)
        
        if token:
            await self.connect_user(token)
            print('usuario conectado enviando lista')
            await self.send_users_online()
            
         
            
        
        
    @database_sync_to_async
    def get_users_online(self):
        profiles = Profile.objects.filter(is_online=True)
        
        users = []
        for profile in profiles:
            users.append(profile.user)
        
        print(list(users))
        return list(users)
    
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
            
    @database_sync_to_async
    def disconnect_user(self, token):
        custom_token = CustomToken.objects.filter(token=token).first()
        authenticated_user = custom_token.user
    # Eliminamos el Profile FALSE
        user_online = Profile.objects.filter(user=authenticated_user).first()
        user_online.is_online = False
        user_online.save()
        
    async def send_users_online(self):
        # Envía la lista de usuarios conectados a todos los clientes
        users_online = await self.get_users_online()
        users_serializer = await user_tojson(users_online)
        await self.send(text_data=json.dumps({
            'type': 'user_list_connect',
            'users': users_serializer
        }))