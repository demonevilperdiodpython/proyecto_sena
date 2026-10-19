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
    # OJO: el default va SIN barra inicial. Con barra ("/users/...") Django la
    # toma como ruta absoluta del sistema, se sale de MEDIA_ROOT y revienta
    # con SuspiciousFileOperation en .url no, pero si en .path, .exists(),
    # .open() y .size. La URL /media sale igual con barra o sin ella, asi que
    # quitarla no cambia nada de lo que se ve, solo deja de estar la trampa.
    imagen = models.ImageField(upload_to='users/avatares', default='users/imagenes/user.jpg')
    score = models.IntegerField(default=0)
    is_banned = models.BooleanField(default=False)
    def clean(self):
        if not self.email.endswith("@gmail.com"):
            from django.core.exceptions import ValidationError
            raise ValidationError("El correo debe ser de Gmail (@gmail.com).")



class imagen(models.Model):
    # Mismo caso que customuser.imagen: sin barra inicial en el default.
    imagen = models.ImageField(upload_to="users/imagenes", default="users/imagenes/user.jpg")
    imagen_url = models.URLField(blank=True, null=True)


