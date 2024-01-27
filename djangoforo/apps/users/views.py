from django.shortcuts import render, redirect
from apps.core.views import get_token, get_userhost
from django.contrib import messages
from .forms import PerfilForm

from django.core.paginator import Paginator
import json, requests


def me_perfil(request):
            
    token = get_token(request)
    user_host = get_userhost(request)
    
    if request.method == 'GET':
        
        url_me = ('http://127.0.0.1:8000/api/authentication/me/')

        url_rooms = ('http://127.0.0.1:8000/api/rooms/my-list/')
        
        
        if token is not None and token != '':
            headers = {
                'Authorization': f'Bearer {token}'
            }
            
            response = requests.get(url_me, headers=headers)
            response_rooms = requests.get(url_rooms, headers=headers)
            
            data = {}
            
            if response.status_code == 200:
                data['me'] = response.json()
                
            if response_rooms.status_code == 200:
                data['allrooms'] = response_rooms.json()
                print(data['allrooms'])

                paginator = Paginator(data['allrooms'], 5)
                
                page = request.GET.get('page')
                
                data['myrooms'] = paginator.get_page(page)
                
                return render(request, 'users/perfil.html',{
                    'token':token,
                    'data':data,
                    'user_host':user_host
                })   
            else:
                return render(request, 'users/perfil.html')
    
    return render(request, 'users/perfil.html') 


def me_perfil_edit(request):
    
    form = PerfilForm()
    token = get_token(request)
    user_host = get_userhost(request)
    
    
    if request.method == 'GET':
        
        url = ('http://127.0.0.1:8000/api/authentication/me/')
    
        if token is not None and token != '':
            
            headers = {
                'Authorization': f'Bearer {token}'
            }
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:           
                data = response.json() 
                print(data)
                
                form = PerfilForm(data=data)
                return render(request, 'users/edit_perfil.html',{
                    'token':token,
                    'form':form,
                    'user_host':user_host
                })
            
        else:
            return render(request, 'users/edit_perfil.html')
    
    elif request.method == 'POST':
        
        url = ('http://127.0.0.1:8000/api/authentication/me/')
        
        if token is not None and token != '':
            
            headers = {
                'Authorization': f'Bearer {token}'
            }
            
            avatar_file = request.FILES.get('avatar')
            files = {'avatar': avatar_file}
            
            response = requests.patch(url, headers=headers, data=request.POST, files=files)
            
            if response.status_code == 200:
                user_data = response.json()
                
                # actualizamos la cookie User
                user_jsonstr = json.dumps(user_data)
                response_html = redirect('me-perfil')
                response_html.set_cookie('User', user_jsonstr)
                messages.success(request, 'Cambios guardados correctamente!')
                
                return response_html
            
def user_view(request, pk):
    
    token = get_token(request)
    user_host = get_userhost(request)
    
    if request.method == 'GET':
        
        url = (f'http://127.0.0.1:8000/api/usersview/usersview/{pk}/')
        url_rooms = (f'http://127.0.0.1:8000/api/rooms/list/{pk}/')
        
        
        if token is not None and token != '':
            
            headers = {
                'Authorization': f'Bearer {token}'
            }
            response = requests.get(url, headers=headers)
            response_rooms = requests.get(url_rooms)
        
            data = {}
            if response.status_code == 200:
                data = response.json()
                
            if response_rooms.status_code == 200:
                data['user_rooms'] = response_rooms.json()
                
                paginator = Paginator(data['user_rooms'], 3)
                page = request.GET.get('page')
                data['user_rooms'] = paginator.get_page(page)

                return render(request, 'users/user_view_copy.html',{
                    'token':token,
                    'user_host': user_host,
                    'data':data,
                })        