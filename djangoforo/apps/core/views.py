from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
import requests
from .forms import LoginForm

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication



#home
def home(request):
    
    if request.method == 'GET':
        url = ('http://127.0.0.1:8000/api/users/')
        
        # Obtener el token guardado en la cookie
        token = request.COOKIES.get('Bearer')
      
        #pasar el token guardado en cookie al header
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if response.status_code == 200:
            return render(request, 'core/home.html', {
                'data':data
            })

    return render(request, 'core/home.html')

def index(request):
    return render(request, 'base.html')

def login(request):
    
    form = LoginForm()
    if request.method == 'POST':
        
        url = ('http://127.0.0.1:8000/api/login/')
        response = requests.post(url, data=request.POST) 
        
        if response.status_code == 200:
            #accedemos al token
            token = response.json()['token']
            
            #lo almacenamos en una cookie
            response_html =  redirect('home')
            response_html.set_cookie('Bearer', token)
            return response_html
            
        elif response.status_code == 401:
            message = response.json()['error']
            return render(request, 'users/login.html', {
                'message':message
            })
        
        elif response.status_code == 404:
            message = response.json()['error'] 
            return render(request, 'users/login.html',{
                'message':message
            })
        
    return render(request, 'users/login.html', {
        'form':form
    })