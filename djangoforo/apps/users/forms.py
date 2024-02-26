from django import forms
from .models import User

class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'bio', 'avatar']
        
        labels = {
            'email': 'Email:',
            'username': 'Username:',
            'bio': 'Biografia:',
            'avatar': 'Foto de perfil:',
            
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 2, 'style': 'width: 100%; resize: none;'}),
        }