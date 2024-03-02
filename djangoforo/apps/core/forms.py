from django import forms 
from apps.users.models import User 

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput())
    
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ('username', 'email', 'password')
        
        labels = {
            'username':'Nombre de usuario',
            'email':'Email',
            'password':'Contraseña'
                
        }
    
        widgets = {
            'password': forms.PasswordInput(),
        }
        