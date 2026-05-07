from django.db import models
from django.conf import settings

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models

class UserSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions"
    )
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    device_id = models.CharField(max_length=128, default="unknown")
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)   
    
    

    def __str__(self):
        return f"{self.user.username} - {self.ip_address}"
    


class customuser(AbstractUser):
    email = models.EmailField(unique=True)
    imagen = models.ImageField(upload_to='imagenes/', blank=True, null=True)
    score = models.IntegerField(default=0)
    is_banned = models.BooleanField(default=False)
    def clean(self):
        if not self.email.endswith("@gmail.com"):
            from django.core.exceptions import ValidationError
            raise ValidationError("El correo debe ser de Gmail (@gmail.com).")



class imagen(models.Model):
    imagen = models.ImageField(upload_to="users/imagenes", default=r"C:\Users\ESTUDIANTE\Desktop\proyecto_sena\project\static\img\user.jpg")
    imagen_url = models.URLField(blank=True, null=True)


