from django.shortcuts import render, redirect
from django.contrib import messages

import requests
from .models import Message
from .forms import RoomForm
from apps.core.views import get_token, get_userhost, set_headers
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


def room_chat(request, pk):
    
    token = get_token(request)
    authenticated_user = get_userhost(request)
    
    if request.method == 'GET':
        
        url = (f'http://127.0.0.1:8000/api/roomsviewset/{pk}/')
        
        headers = set_headers(token)
        
        if headers:  
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                
                data = response.json()              
                ms = Message.objects.filter(room=data['room']['id'])
                
                data['ms'] = ms
                return render(request, 'rooms/room_chat.html',{
                    'authenticated_user':authenticated_user,
                    'token':token,
                    'data':data,
                    
                })
                
        else:
            response = requests.get(url)
            data = response.json()  
            ms = Message.objects.filter(room=data['room']['id'])
                
            data['ms'] = ms
            
            return render(request, 'rooms/room_chat.html',{
                    'authenticated_user':authenticated_user,
                    'data':data,
                    
                })
            
                


def room_create(request):
    
    token = get_token(request)
    authenticated_user = get_userhost(request)
    
    form = RoomForm()
    
    if request.method == 'GET':
        
        
        return render(request, 'rooms/room_create.html',{
            'token':token,
            'authenticated_user':authenticated_user,
            'form':form
        })
    
    if request.method == 'POST':
        
        url = ('http://127.0.0.1:8000/api/rooms/create/')
        
        headers = set_headers(token)
        
        if headers:  
       
            file_image = request.FILES.get('image')
     
            files = {'image': file_image}

        
            response = requests.post(url, headers=headers, data=request.POST, files=files)
            
            if response.status_code == 201:
                message = response.json()['message']

                messages.success(request, message)
                
                return redirect ('home')
                
            else:
                message = response.json()
                return render(request, 'rooms/room_create.html')
                

    return render(request, 'rooms/room_create.html')

def room_edit_delete(request, pk):
        
    token = get_token(request)
    authenticated_user = get_userhost(request)
    form = RoomForm()
    
    if request.method == 'GET':
        
        url = (f'http://127.0.0.1:8000/api/rooms/my-list/{pk}/')
      
        headers = set_headers(token)
        
        if headers:  
                 
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
       
                form = RoomForm(data=data)
                
                return render(request, 'rooms/room_edit.html', {
                    'token':token,
                    'authenticated_user':authenticated_user,
                    'form':form,
                    'data':data
                })
            
    if request.method == 'POST':
        
        url = (f'http://127.0.0.1:8000/api/rooms/my-list/{pk}/')
        action = request.POST.get('action')
        if action == 'edit':
        
            headers = set_headers(token)
        
            if headers:  
                
                                
                file_image = request.FILES.get('image')
            
                #if file_image is not None:
                files = {'image': file_image}
                #else:
                #    files = {}
                
                response = requests.patch(url, headers=headers, data=request.POST, files=files)
                
                if response.status_code == 200:
                    message = ('Room edit correctamente!')
                    messages.success(request, message)
            
                else:
                    message = ('Error')
                    messages.error(request, message)
        
                return redirect ('me-perfil')

            
            
        elif action == 'delete':
       
            
            headers = set_headers(token)
        
            if headers:  
                response = requests.delete(url, headers=headers)


                if response.status_code == 204:
                    message = 'Room eliminado correctamente!'
                    messages.success(request, message)
                    return redirect('me-perfil')

        else:
            return redirect('me-perfil')




def room_like(request, pk):
    
    token = get_token(request)
    
    if request.method == 'POST':
        
        url = (f'http://127.0.0.1:8000/api/roomsviewset/{pk}/like-room/')
        
        headers = set_headers(token)
        
        if headers:  
            
            response = requests.post(url, headers=headers)
            
            if response.status_code == 200:
                message = response.json()['message']
                messages.success(request, message)
                return redirect('home')
            
            else:
                message = 'Error al dar like'
                return redirect('home')


            



