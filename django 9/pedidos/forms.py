from django import forms

from .models import PedidoDetalle


class PedidoDetalleForm(forms.ModelForm):
    class Meta:
        model = PedidoDetalle
        fields = ['producto', 'cantidad']

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')
        if producto is not None and cantidad is not None:
            if cantidad > producto.stock:
                raise forms.ValidationError(
                    f'No hay stock suficiente de "{producto.nombre}". '
                    f'Stock disponible: {producto.stock}.'
                )
        return cleaned_data
