from .models import producto
from django import forms
from .models import post
from .models import topics_group
from .models import topic_section

class productoForm(forms.ModelForm):
    imagen = forms.ImageField(required=False)
    imagen_url = forms.URLField(required=False)
    class Meta:
        model = producto
        fields = '__all__'
        
        

class topic_groupForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nombre"].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ' ',
            'label': 'name'
            })
        
        self.fields["imagen"].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ' ',
            'label': 'imagen'
        }
        )
        self.fields["imagen_url"].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ' ',
            'label': 'imagen_url'
        })
    imagen = forms.ImageField(required=False)
    imagen_url = forms.URLField(required=False)
    class Meta:
        model = topics_group
        fields = ('nombre', 'categoria', 'imagen','imagen_url')
class postForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, required=True)
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["content"].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Escribe tu post aquí...',
            
    })
    class Meta:
        model = post
        fields = ['content']


