from django.shortcuts import render, redirect
from apps.core.views import get_token

import json, requests

def me_perfil(request):
    
    if request.method == 'GET':
        
        url = ('http://127.0.0.1:8000/api/me/')
        
        token = get_token(request)
        
        if token is not None and token != '':
            headers = {
                'Authorization': f'Bearer {token}'
            }
            
            response = requests.get(url, headers=headers)
            
            data = response.json()
            print(data)
            return render(request, 'users/perfil.html',{
                'token':token,
                'data':data
            })   
    
    return render(request, 'users/perfil.html') 
        