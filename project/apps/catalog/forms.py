from django import forms
from .models import post
from .models import topics_group
from .models import topic_section


class topic_groupForm(forms.ModelForm):
    descripcion = forms.CharField(required=False, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nombre"].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ' ',
            'label': 'name'
            })

        # El campo descripcion se agrego al modelo: se pinta como textarea.
        self.fields["descripcion"].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ' ',
            'label': 'descripcion',
            'rows': 3,
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
        fields = ('nombre', 'descripcion', 'categoria', 'imagen', 'imagen_url')


class postForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["content"].widget.attrs.update({
            'class': 'form-control',

    })
    class Meta:
        model = post
        fields = ['content']
