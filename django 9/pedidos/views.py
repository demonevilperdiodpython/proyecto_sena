from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PedidoDetalleForm
from .models import Pedido, PedidoDetalle


def crear_pedido(request):
    if request.method == 'POST':
        pedido = Pedido.objects.create()
        messages.success(request, 'Pedido creado correctamente.')
        return redirect('agregar_producto_pedido', pk=pedido.pk)
    return render(request, 'pedidos/crear.html')


def agregar_producto_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        form = PedidoDetalleForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.pedido = pedido
            detalle.save()
            messages.success(request, 'Producto agregado al pedido correctamente.')
            return redirect('agregar_producto_pedido', pk=pedido.pk)
    else:
        form = PedidoDetalleForm()
    detalles = pedido.pedidodetalle_set.all()
    return render(
        request,
        'pedidos/detalle.html',
        {'pedido': pedido, 'form': form, 'detalles': detalles},
    )


def eliminar_detalle_pedido(request, pedido_pk, pk):
    detalle = get_object_or_404(PedidoDetalle, pk=pk, pedido_id=pedido_pk)
    if request.method == 'POST':
        detalle.delete()
        messages.success(request, 'Producto eliminado del pedido correctamente.')
        return redirect('agregar_producto_pedido', pk=pedido_pk)
    return render(request, 'pedidos/eliminar_detalle.html', {'detalle': detalle})
