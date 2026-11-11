from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import customuser as CustomUser
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    imagen = forms.ImageField(required=False)

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["username"].widget.attrs.update({
            'class': 'Form-control',
            'placeholder': ' '
            })
        self.fields["password1"].widget.attrs.update({
            'class': 'Form-control',
            'placeholder': ' '
        })
        self.fields["password2"].widget.attrs.update({
            'class': 'Form-control',
            'label': "confirmar contraseña",
            'placeholder': ' '})
        
        self.fields["email"].widget.attrs.update({
            'class': 'Form-control',
            'type': 'email',
            'placeholder': ' '
        })
        self.fields["imagen"].widget.attrs.update({
            'class': "img-imput",
            'file': "image/*",
            'placeholder': ' ',
            'id': 'id_imagen'
            
        })
        self.fields["username"].label = "username"
        self.fields["password2"].label = "password"
        self.fields["password1"].label = "password"
        self.fields["email"].label = "email"
        self.fields["imagen"].label = "profile picture"

        self.fields["username"].error_messages = {
            'required': 'El nombre de usuario es obligatorio.',
            'unique': 'Este nombre de usuario ya está en uso.',
            'max_length': 'El nombre de usuario es demasiado largo.',
        }
        self.fields["password1"].error_messages = {
            'required': 'La contraseña es obligatoria.',
        }
        self.fields["password2"].error_messages = {
            'required': 'Debes confirmar la contraseña.',
            'password_mismatch': 'Las contraseñas no coinciden.',
        }
    email = forms.EmailField(required=True, error_messages={
        'required': 'El correo es obligatorio.',
        'invalid': 'Ingresa un correo válido.',
    })
    

    class Meta:
        model = CustomUser
        
        
        fields = ("username", "email", "password1", "password2", "imagen")
        

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith("@gmail.com"):
            raise forms.ValidationError("El correo debe ser de Gmail (@gmail.com).")
        return email  
    def label_tag(self, name=None, attrs=None, contents=None, label_suffix=None):
        attrs = attrs or {}
        attrs['class'] = 'mi-clase-label'
        return super().label_tag(name, attrs=attrs, contents=contents, label_suffix=label_suffix)
    
    
class CustomAuthenticationForm(AuthenticationForm): 
    def __init__(self,*args, user=None, **kwargs):
        username = user
        super().__init__(*args, **kwargs)
        
        self.fields["username"].label = "username or email"
        self.fields["password"].label = "password"
        
        
        
        if username:
            self.fields["username"].initial = username
            self.fields["username"].label = ""
            self.fields["username"].widget = forms.HiddenInput()
        else:
            self.fields["username"].widget.attrs.update({
                'class': 'Form-control',
                'placeholder': ' '
                    
                })
        self.fields["password"].widget.attrs.update({
            'class': 'Form-control',
            'placeholder': ' '
        })

        self.fields["username"].error_messages = {
            'required': 'El usuario o correo es obligatorio.',
        }
        self.fields["password"].error_messages = {
            'required': 'La contraseña es obligatoria.',
        }
        
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
                return user.username
            except CustomUser.DoesNotExist:
                raise forms.ValidationError(
                    "no hay cuenta creada con este gmail"
                )
        else:
            return username
    def label_tag(self, name=None, attrs=None, contents=None, label_suffix=None):
        attrs = attrs or {}
        attrs['class'] = 'mi-clase-label'
        return super().label_tag(name, attrs=attrs, contents=contents, label_suffix=label_suffix)
            