from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.IntegerField(validators=[MinValueValidator(1)])
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    precio_oferta = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1)]
    )

    def clean(self):
        super().clean()
        if self.precio_oferta is not None and self.precio_oferta >= self.precio:
            raise ValidationError(
                'El precio de oferta debe ser menor que el precio normal.'
            )

    def __str__(self):
        return self.nombre
