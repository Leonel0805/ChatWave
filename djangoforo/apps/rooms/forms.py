from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room 
        fields = ['name', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'cols':60}),
        }
