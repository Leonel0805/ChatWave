from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import LoginForm, RegisterForm

from django.core.paginator import Paginator 

import json, requests

# Home

def get_token(request):
    token = request.COOKIES.get('Bearer')
    return token

def get_userhost(request):
    user_host_jsonstr = request.COOKIES.get('User')
    
    if user_host_jsonstr is not None:
        #convertimos el userstr en objeto dict 
        user = json.loads(user_host_jsonstr)
        return user

def home(request):
    
    if request.method == 'GET':
      
        url_users = ('http://127.0.0.1:8000/api/usersview/usersview/')
        url_rooms = ('http://127.0.0.1:8000/api/rooms/list/')
        url_liked_rooms = ('http://127.0.0.1:8000/api/rooms/list/liked_rooms/')
        
        # Obtener el token guardado en la cookie
        token = get_token(request)
        
        #obtenemos el user guardado en cookie
        user_host = get_userhost(request)
        
        #pasar el token guardado en cookie al header
        #if token is not None and token != '':
        headers = {
                'Authorization': f'Bearer {token}'
            }
        
        response_users = requests.get(url_users, headers=headers)
        response_rooms = requests.get(url_rooms, headers=headers)
        response_likes_rooms = requests.get(url_liked_rooms, headers=headers)
            
        data = {}
            
        if response_likes_rooms.status_code == 200:
            data['all_likedrooms'] = response_likes_rooms.json()
            
            paginator2 = Paginator(data['all_likedrooms'], 5)
            page2 = request.GET.get('page2')
            data['likedrooms'] = paginator2.get_page(page2)
            print(data['likedrooms'])
            
        if response_users.status_code == 200:
            data['users'] = response_users.json()
                
        if response_rooms.status_code == 200:
            data['allrooms'] = response_rooms.json()
                
            paginator = Paginator(data['allrooms'], 5)
                
            page = request.GET.get('page')
                
            data['rooms'] = paginator.get_page(page)          
                
            if 'success_message_displayed' not in request.session:
                messages.success(request, 'usuarios cargados correctamente')
                request.session['success_message_displayed'] = True
                
            return render(request, 'core/home.html', {
                'user_host':user_host,
                'token':token,
                'data':data
    
            })
                
        elif response_users.status_code == 401:
                
            error = response_users.json()['messages'][0]['message']
            messages.error(request, error)
                
    return render(request, 'core/home.html')


def search(request):
    
    token = get_token(request)
    user_host = get_userhost(request)
    
    if request.method == 'GET':
        
        url = ('http://127.0.0.1:8000/api/rooms/search/')
        
        #obtenemos lo enviado por el form de search en la navbar
        query = request.GET.get('query', '')
        
        if token is not None and token != '':
            
            headers = {
                'Authorization': f'Bearer {token}'
            }
            
            #lo enviamos como params haciendo un get a la url
            params = {'search': query}
            response = requests.get(url, headers=headers, params=params)
            
            data = {}
            if response.status_code == 200:
                data['rooms'] = response.json() 
                
                return render(request, 'core/search.html',{
                    'token':token,
                    'user_host':user_host,
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
    

def logout(request):
    
    if request.method == 'POST':
        
        url = ('http://127.0.0.1:8000/api/authentication/logout/')
        
        
        token = get_token(request)
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            message = response.json()['message']
            messages.success(request, message)
            response_html = redirect ('register')
            response_html.set_cookie('Bearer', value='')
            return response_html
        
        else:
            print('no 200')
    
    return render(request, 'users/logout.html')
            
            
