from django import forms 
from apps.users.models import User 

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ('username', 'email', 'password')