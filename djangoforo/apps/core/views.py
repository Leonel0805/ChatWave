from django.shortcuts import render, redirect
import requests
from .forms import LoginForm

#home
def home(request):

    return render(request, 'core/home.html')

def index(request):
    return render(request, 'base.html')

def login(request):
    
    form = LoginForm()
    if request.method == 'POST':
        
        url = ('http://127.0.0.1:8000/api/login/')
        response = requests.post(url, data=request.POST) 
        
        if response.status_code == 200:
            return redirect('home')
            
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