from django.shortcuts import render
import requests

from apps.core.views import get_token, get_userhost

def room_chat(request, pk):
    
    token = get_token(request)
    user_host = get_userhost(request)
    
    url = (f'http://127.0.0.1:8000/api/roomsviewset/{pk}/')
    
    if token is not None and token != '':
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        response = requests.get(url, headers=headers)
        
        
        if response.status_code == 200:
                
            data = response.json()
            
            return render(request, 'rooms/room_chat.html',{
                'token':token,
                'user_host':user_host,
                'data':data
                
            })


def room_like(request):
    pass
