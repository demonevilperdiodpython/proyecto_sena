from .models import producto
from django import forms

class productoForm(forms.ModelForm):
    imagen = forms.ImageField(required=False)
    imagen_url = forms.URLField(required=False)
    class Meta:
        model = producto
        fields = '__all__'
        
        

    