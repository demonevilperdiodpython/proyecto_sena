from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import orderlistdetalleForm
from .models import orderlist, orderlistdetalle


def crear_pedido(request):
    if request.method == 'POST':
        pedido = orderlist.objects.create(
            user=request.user if request.user.is_authenticated else None
        )
        messages.success(request, 'Pedido creado correctamente.')
        return redirect('orders:agregar_producto_pedido', pk=pedido.pk)
    return render(request, 'orders/crear.html')


def agregar_producto_pedido(request, pk):
    pedido = get_object_or_404(orderlist, pk=pk)
    if request.method == 'POST':
        form = orderlistdetalleForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.orderlist = pedido
            detalle.save()
            messages.success(request, 'Producto agregado al pedido correctamente.')
            return redirect('orders:agregar_producto_pedido', pk=pedido.pk)
    else:
        form = orderlistdetalleForm()
    detalles = pedido.detalles.all()
    return render(
        request,
        'orders/detalle.html',
        {'pedido': pedido, 'form': form, 'detalles': detalles},
    )


def eliminar_detalle_pedido(request, pedido_pk, pk):
    detalle = get_object_or_404(orderlistdetalle, pk=pk, orderlist_id=pedido_pk)
    if request.method == 'POST':
        detalle.delete()
        messages.success(request, 'Producto eliminado del pedido correctamente.')
        return redirect('orders:agregar_producto_pedido', pk=pedido_pk)
    return render(request, 'orders/eliminar_detalle.html', {'detalle': detalle})
