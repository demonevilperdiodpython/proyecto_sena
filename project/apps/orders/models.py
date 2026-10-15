from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.catalog.models import producto


class orderlist(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'Pedido {self.pk}'


class orderlistdetalle(models.Model):
    orderlist = models.ForeignKey(
        orderlist,
        on_delete=models.CASCADE,
        related_name='detalles',
    )
    producto = models.ForeignKey(producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=1)

    def clean(self):
        super().clean()
        if self.producto_id and self.cantidad is not None:
            if self.cantidad > self.producto.stock:
                raise ValidationError(
                    {
                        'cantidad': (
                            f'No hay stock suficiente de "{self.producto.nombre}". '
                            f'Stock disponible: {self.producto.stock}.'
                        )
                    }
                )

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'
