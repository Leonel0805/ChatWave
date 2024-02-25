from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import LoginForm, RegisterForm

from django.core.paginator import Paginator 
from apps.users.models import CustomToken

import json, requests


# Funciones token, authenticated_user

# Obtenemos el Bearer token, despues de setearlo en el /login
def get_token(request):
    token = request.COOKIES.get('Bearer')
    return token

#Seteamos header con token
def set_headers(token):
    if token is not None and token != '':
        return {'Authorization': f'Bearer {token}'}
    return None

#Obtenemos User autenticado
def get_userhost(request):
    bearer_token = request.COOKIES.get('Bearer')

    token = CustomToken.objects.filter(token=bearer_token).first()
    
    if token:
        user = token.user
        return user
    
    return None

# Home
def home(request):
    
    if request.method == 'GET':
      
        url_users = ('http://127.0.0.1:8000/api/authentication/users/')
        url_rooms = ('http://127.0.0.1:8000/api/rooms/list/')
        url_liked_rooms = ('http://127.0.0.1:8000/api/rooms/list/liked_rooms/')
        
        # Obtener el token, user guardado en la cookies
        token = get_token(request)
        authenticated_user = get_userhost(request)
        
        # Pasar el token guardado en cookie al header
        headers = set_headers(token)
        
        if headers is None:
            response_users = requests.get(url_users)
        else:
            response_users = requests.get(url_users, headers=headers)
            
        response_rooms = requests.get(url_rooms, headers=headers)
        response_likes_rooms = requests.get(url_liked_rooms, headers=headers)
            
        data = {}
            
        if response_likes_rooms.status_code == 200:
            data['all_likedrooms'] = response_likes_rooms.json()
      
            paginator3 = Paginator(data['all_likedrooms'], 5)
            page3 = request.GET.get('page3')
            data['likedrooms'] = paginator3.get_page(page3)
           
        if response_rooms.status_code == 200:
            data['allrooms'] = response_rooms.json()
   
            paginator2 = Paginator(data['allrooms'], 5) 
            page2 = request.GET.get('page2')
            data['rooms'] = paginator2.get_page(page2)  
                
        if response_users.status_code == 200:
            data['all_users'] = response_users.json()
            
            paginator = Paginator(data['all_users'], 5)
            page = request.GET.get('page')
            data['users'] = paginator.get_page(page)   
            
            return render(request, 'core/home.html', {
                'authenticated_user':authenticated_user,
                'token':token,
                'data':data
    
            })
                
        elif response_users.status_code == 401:
                
            error = response_users.json()['messages'][0]['message']
            messages.error(request, error)
                
    return render(request, 'core/home.html')

# Search
def search(request):
    
    token = get_token(request)
    authenticated_user = get_userhost(request)
    
    if request.method == 'GET':
        
        url = ('http://127.0.0.1:8000/api/rooms/search/')
        
        #obtenemos lo enviado por el form de search en la navbar
        query = request.GET.get('query', '')
        
        headers = set_headers(token)
        
        if headers:    
            #lo enviamos como params haciendo un get a la url
            params = {'search': query}
            response = requests.get(url, headers=headers, params=params)
            
            data = {}
            if response.status_code == 200:
                data['rooms'] = response.json() 
                
                return render(request, 'core/search.html',{
                    'token':token,
                    'authenticated_user':authenticated_user,
                    'data':data
                })
        
        
    
def index(request):
    return render(request, 'base.html')

# Register
def register(request):
    
    form = RegisterForm()
    
    if request.method == 'GET':
        return render(request, 'users/register.html',{
        'form':form
    })    

    if request.method == 'POST':
        
        url = ('http://127.0.0.1:8000/api/authentication/register/')
        response = requests.post(url, data=request.POST)
        
        if response.status_code == 201:
            message = response.json()['message']       
            messages.success(request, message)
            
            return redirect('login')
    
        elif response.status_code == 400:
            errors = response.json()['errors']
            
            for ms in errors.values():
                for message in ms:
                    messages.error(request, message)
                
            form = RegisterForm(data=request.POST)
     
            return render(request, 'users/register.html',{
                'form':form
            })
    

# Login
def login(request):
    
    form = LoginForm()
        
    if request.method == 'POST':
        
        url = ('http://127.0.0.1:8000/api/authentication/login/')
        response = requests.post(url, data=request.POST) 
        
        if response.status_code == 200:
            #accedemos al token
            token = response.json()['token']
            # user = response.json()['user']
            message = response.json()['message']
            
            #lo almacenamos en una cookie
            response_html =  redirect('home')
            response_html.set_cookie('Bearer', token)
            
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
    
# Logout
def logout(request):
    
    token = get_token(request)
    authenticated_user = get_userhost(request)
    
    
    if request.method == 'POST':
        
        url = ('http://127.0.0.1:8000/api/authentication/logout/')
        
        
        headers = set_headers(token)
        
        if headers:  
            response = requests.post(url, headers=headers)

            if response.status_code == 200:
                message = response.json()['message']
                messages.success(request, message)
                response_html = redirect ('login')
                
                # user_logout = CustomToken.objects.filter(user=authenticated_user).first()
                # print(user_logout)
                
                response_html.set_cookie('Bearer', value='')
                print(authenticated_user)
                # user_logout.delete()
                
                return response_html
            
    
    return render(request, 'users/logout.html', {
        'token':token,
        'authenticated_user':authenticated_user,
        
    })
    
            
            
