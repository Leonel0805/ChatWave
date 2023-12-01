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
     
            #validacion file_image is not None, esta en el serializer
            files = {'image': file_image}

        
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

def room_edit_delete(request, pk):
        
    token = get_token(request)
    user_host = get_userhost(request)
    form = RoomForm()
    
    if request.method == 'GET':
        
        url = (f'http://127.0.0.1:8000/api/rooms/my-list/{pk}/')
      
        
        if token is not None and token != '':
                
            headers = {
                'Authorization': f'Bearer {token}'
            }
                 
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
       
                form = RoomForm(data=data)
                
                return render(request, 'rooms/room_edit.html', {
                    'token':token,
                    'user_host':user_host,
                    'form':form
                })
            
    if request.method == 'POST':
        
        url = (f'http://127.0.0.1:8000/api/rooms/my-list/{pk}/')
        action = request.POST.get('action')
        
        if action == 'edit':
        
            if token is not None and token != '':
                
                headers = {
                    'Authorization': f'Bearer {token}'
                }
                
                                
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
       
            
            if token is not None and token != '':
                
                headers = {
                    'Authorization': f'Bearer {token}'
                }
                
                response = requests.delete(url, headers=headers)


                if response.status_code == 204:
                    message = 'Room eliminado correctamente!'
                    messages.success(request, message)
                    return redirect('me-perfil')




def room_like(request, pk):
    
    token = get_token(request)
    user_host = get_userhost(request)
    
    if request.method == 'POST':
        
        url = (f'http://127.0.0.1:8000/api/roomsviewset/{pk}/like-room/')
        
        if token is not None and token != '':
             
            headers = {
                'Authorization': f'Bearer {token}'
            }
            
            response = requests.post(url, headers=headers)
            
            if response.status_code == 200:
                message = response.json()['message']
                messages.success(request, message)
                return redirect('home')
            
            else:
                message = 'Error al dar like'
                return redirect('home')

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



