from django import forms
from .models import User

class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'cols': 60}),
        }