from django.core.exceptions import ValidationError
from django.db import models
from productos.models import Producto


class Pedido(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(default=0)

    def __str__(self):
        return f'Pedido {self.pk}'


class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
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
