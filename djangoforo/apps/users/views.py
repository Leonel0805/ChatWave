from django.shortcuts import render, redirect
from apps.core.views import get_token
from django.contrib import messages
from .forms import PerfilForm

import json, requests


def me_perfil(request):
    
    if request.method == 'GET':
        
        url = ('http://127.0.0.1:8000/api/authentication/me/')
        
        token = get_token(request)
        
        if token is not None and token != '':
            headers = {
                'Authorization': f'Bearer {token}'
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                
                data = response.json()     
                return render(request, 'users/perfil.html',{
                    'token':token,
                    'data':data
                })   
            else:
                return render(request, 'users/perfil.html')
    
    return render(request, 'users/perfil.html') 


def me_perfil_edit(request):
    
    form = PerfilForm()
    token = get_token(request)
    
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
                    'form':form
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
                messages.success(request, 'Cambios guardados correctamente!')
                return redirect ('me-perfil')