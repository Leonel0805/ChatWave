from django.shortcuts import render, redirect
from django.contrib import messages

import requests


from .forms import RoomForm
from apps.core.views import get_token, get_userhost

def room_create(request):
    
    token = get_token(request)
    user_host = get_userhost(request)
    
    form = RoomForm()
    
    if request.method == 'GET':
        return render(request, 'rooms/room_create.html',{
            'token':token,
            'user_host':user_host,
            'form':form
        })
    
    if request.method == 'POST':
        
        url = ('http://127.0.0.1:8000/api/rooms/create/')
        
        if token is not None and token != '':
            
            headers = {
                'Authorization': f'Bearer {token}'
            }
            
       
            file_image = request.FILES.get('image')
            
            if file_image is not None:
                files = {'image': file_image}
            else:
                print('no se proporciono nada')
                files = {}
        
            response = requests.post(url, headers=headers, data=request.POST, files=files)
            
            if response.status_code == 201:
                message = response.json()
                print(message)
                print(message)
                messages.success(request, message)
                
                return redirect ('home')
                
            else:
                message = response.json()
                print(message)
                return render(request, 'rooms/room_create.html')
                

    return render(request, 'rooms/room_create.html')



def room_like(request):
    pass

def room_chat(request, pk):
    
    token = get_token(request)
    user_host = get_userhost(request)
    
    if request.method == 'GET':
        
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
            
            return render(request, 'rooms/room_chat.html')



