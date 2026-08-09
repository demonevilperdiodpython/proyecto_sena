
import requests
from django.core.files.base import ContentFile
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from .forms import CustomUserCreationForm as UserForm
from .models import customuser

class CustomSocialAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        email = data.get('email') or sociallogin.account.extra_data.get('email')
        if email:
            user.email = email
        return user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        
        avatar_url = sociallogin.account.extra_data.get('picture', '')
        if avatar_url and hasattr(user, 'imagen'):
            try:
                response = requests.get(avatar_url, timeout=5)
                if response.status_code == 200:
                    file_name = f"google_avatar_{user.id}.jpg"
                    user.imagen.save(file_name, ContentFile(response.content), save=True)
            except Exception:
                pass
        
        return user