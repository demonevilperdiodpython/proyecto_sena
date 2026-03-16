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
    login_time = models.DateTimeField(default="2025-01-01")
    is_active = models.BooleanField(default=True)    

    def __str__(self):
        return f"{self.user.username} - {self.ip_address}"
    


class customuser(AbstractUser):
    email = models.EmailField(unique=True)

    def clean(self):
        if not self.email.endswith("@gmail.com"):
            from django.core.exceptions import ValidationError
            raise ValidationError("El correo debe ser de Gmail (@gmail.com).")