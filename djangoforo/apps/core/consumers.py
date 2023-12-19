import json 

from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    
    #nos conectamos
    async def connect(self):
        self.room_name = self.scope ['url_route']['kwargs']['pk']
        self.room_group_name = f'chat_ {self.room_name}'
        
    
        await self.channel_layer(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()