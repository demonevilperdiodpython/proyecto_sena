from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from project.paths import ruta_con_fecha


class UserSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions",
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

    # Avatar del usuario. Se guarda en users/avatares/<fecha>/<uuid>.ext para
    # no acumular duplicados. El default vive en la misma carpeta.
    imagen = models.ImageField(
        upload_to=ruta_con_fecha("users/avatares"),
        default="users/avatares/user.jpg",
    )
    score = models.IntegerField(default=0)
    is_banned = models.BooleanField(default=False)

    def clean(self):
        if not self.email.endswith("@gmail.com"):
            from django.core.exceptions import ValidationError

            raise ValidationError("El correo debe ser de Gmail (@gmail.com).")

    def recalcular_score(self):
        post_score = sum(p.score for p in self.post_set.all()) if hasattr(self, "post_set") else 0
        group_score = sum(g.score for g in self.created_groups.all()) if hasattr(self, "created_groups") else 0
        self.score = post_score + group_score
        self.save(update_fields=["score"])
        return self.score


class imagen(models.Model):
    # Galeria de imagenes predeterminadas para el avatar. Misma carpeta que
    # el default para no mezclar con otros archivos.
    imagen = models.ImageField(
        upload_to=ruta_con_fecha("users/imagenes"),
        default="users/imagenes/user.jpg",
    )
    imagen_url = models.URLField(blank=True, null=True)
