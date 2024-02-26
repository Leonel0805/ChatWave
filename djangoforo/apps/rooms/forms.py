from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room 
        fields = ['name', 'description', 'image']
        
        labels = {
            'name': 'Nombre de la sala:',
            'description': 'Descripción de la sala:',
            'image': 'Portada de la sala:',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'style': 'width: 100%; resize: none;'}),
        }
