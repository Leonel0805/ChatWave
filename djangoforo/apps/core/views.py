from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import LoginForm, RegisterForm

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

import json
import requests

# Home
def home(request):
    
    if request.method == 'GET':
      
        url = ('http://127.0.0.1:8000/api/usersview/usersview/')
        
        # Obtener el token guardado en la cookie
        token = request.COOKIES.get('Bearer')
        
        #obtenemos el user guardado en cookie
        user_jsonstr = request.COOKIES.get('User')
        
        #convertimos el user type str a dict 
        user = json.loads(user_jsonstr)
        print(user['username'])
        
        #pasar el token guardado en cookie al header
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        response = requests.get(url, headers=headers)
        data = response.json()
        print(data)
        
        if response.status_code == 200:
            messages.success(request, 'usuarios cargados correctamente')
            
            return render(request, 'core/home.html', {
                'data':data,
                'user':user
            })
            
        else:
            error = response.json()['messages'][0]['message']
            messages.error(request, error)
            
    return render(request, 'core/home.html')


def index(request):
    return render(request, 'base.html')

# Register
def register(request):
    
    form = RegisterForm()

    if request.method == 'POST':
        
        url = ('http://127.0.0.1:8000/api/register/')
        response = requests.post(url, data=request.POST)
        
        if response.status_code == 201:
            message = response.json()['message']       
            messages.success(request, message)
            
            return redirect('login')
    
        else:
            error = response.json()['error']       
            messages.error(request, error)
    
    return render(request, 'users/register.html',{
        'form':form
    })    
    

# Login
def login(request):
    
    form = LoginForm()
    
    if request.method == 'POST':
        
        url = ('http://127.0.0.1:8000/api/login/')
        response = requests.post(url, data=request.POST) 
        
        if response.status_code == 200:
            #accedemos al token
            token = response.json()['token']
            user = response.json()['user']
            message = response.json()['message']
            
            #convertimos el objeto a str json
            user_jsonstr = json.dumps(user)
            #lo almacenamos en una cookie
            response_html =  redirect('home')
            response_html.set_cookie('Bearer', token)
            response_html.set_cookie('User', user_jsonstr)
            
            messages.success(request, message)
            
            return response_html
            
        elif response.status_code == 401:
            error = response.json()['error']
            messages.error(request, error)
        
        elif response.status_code == 404:
            error = response.json()['error'] 
            messages.error(request, error)
            
        
    return render(request, 'users/login.html', {
        'form':form,
    })