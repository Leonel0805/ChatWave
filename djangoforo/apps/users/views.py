from django.shortcuts import render, redirect
from apps.core.views import get_token, get_userhost, set_headers
from django.contrib import messages
from .forms import PerfilForm
from apps.users.models import User

from django.core.paginator import Paginator
import json, requests


def me_perfil(request):
            
    token = get_token(request)
    authenticated_user = get_userhost(request)
    
    if request.method == 'GET':
        
        url_me = ('http://127.0.0.1:8000/api/authentication/me/')

        url_rooms = ('http://127.0.0.1:8000/api/rooms/my-list/')
        
        
        headers = set_headers(token)
        
        if headers:  
            response = requests.get(url_me, headers=headers)
            response_rooms = requests.get(url_rooms, headers=headers)
            
            data = {}
            
            if response.status_code == 200:
                
                data['me'] = response.json()
                del data['me']['id']
                data['verbose_name'] = User._meta.get_field('avatar').verbose_name
                
            if response_rooms.status_code == 200:
                data['allrooms'] = response_rooms.json()

                paginator = Paginator(data['allrooms'], 4)
                
                page = request.GET.get('page')
                
                data['myrooms'] = paginator.get_page(page)
                
                return render(request, 'users/perfil.html',{
                    'token':token,
                    'data':data,
                    'authenticated_user':authenticated_user
                })   
            else:
                return render(request, 'users/perfil.html')
    
    return render(request, 'users/perfil.html') 


def me_perfil_edit(request):
    
    form = PerfilForm()
    token = get_token(request)
    authenticated_user = get_userhost(request)
    
    
    if request.method == 'GET':
        
        url = ('http://127.0.0.1:8000/api/authentication/me/')
    
        headers = set_headers(token)
        
        if headers:  
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:           
                data = response.json() 
                form = PerfilForm(data=data)
                return render(request, 'users/edit_perfil.html',{
                    'token':token,
                    'form':form,
                    'authenticated_user':authenticated_user
                })
            
        else:
            return render(request, 'users/edit_perfil.html',{
                'form':form
            })
    
    elif request.method == 'POST':
        
        url = ('http://127.0.0.1:8000/api/authentication/me/')
        
        headers = set_headers(token)
        
        if headers:  
            
            form = PerfilForm(request.POST, request.FILES)
            # if form.is_valid():
            avatar_file = request.FILES.get('avatar')
            files = {'avatar': avatar_file}
            
            response = requests.patch(url, headers=headers, data=request.POST, files=files)
            
            if response.status_code == 200:

                response_html = redirect('me-perfil')
                messages.success(request, 'Cambios guardados correctamente!')
                return response_html
            
            else:
                errors = {}
                for error in response.json():
                    errors[error] = response.json()[error]
                    
                return render(request, 'users/edit_perfil.html', {'form': form, 'errors_form':errors})
             
             
def me_perfil_change_password(request):
    
    token = get_token(request)
    authenticated_user = get_userhost(request)
    
    form = PerfilForm()
    
    if request.method == 'POST':
        url = ('http://127.0.0.1:8000/api/authentication/me/change-password/')
        
    return render(request, 'users/edit_perfil_password.html',{
        'form': form,
        'token':token,
        'authenticated_user':authenticated_user
    })
            
def user_view(request, pk):
    
    token = get_token(request)
    authenticated_user = get_userhost(request)
    
    if request.method == 'GET':
        
        url = (f'http://127.0.0.1:8000/api/usersview/usersview/{pk}/')
        url_rooms = (f'http://127.0.0.1:8000/api/rooms/list/{pk}/')
        
        
        headers = set_headers(token)
        
        if headers:  
            response = requests.get(url, headers=headers)
            response_rooms = requests.get(url_rooms)
        
            data = {}
            if response.status_code == 200:
                data = response.json()
                
            if response_rooms.status_code == 200:
                data['user_allrooms'] = response_rooms.json()

                paginator_rooms = Paginator(data['user_allrooms'], 3)
                page_rooms = request.GET.get('page_rooms')
                data['user_rooms'] = paginator_rooms.get_page(page_rooms)
                
                return render(request, 'users/user_view.html',{
                    'token':token,
                    'authenticated_user': authenticated_user,
                    'data':data,
                })        
            
            else: 
     
                data['message'] = response_rooms.json()['message']
                
                return render(request, 'users/user_view.html',{
                    'token':token,
                    'authenticated_user': authenticated_user,
                    'data':data,
                })   
                
                