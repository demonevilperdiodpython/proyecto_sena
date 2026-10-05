from django.urls import path

from . import views

urlpatterns = [
    path('pedidos/nuevo/', views.crear_pedido, name='crear_pedido'),
    path('pedidos/<int:pk>/agregar/', views.agregar_producto_pedido, name='agregar_producto_pedido'),
    path(
        'pedidos/<int:pedido_pk>/detalle/<int:pk>/eliminar/',
        views.eliminar_detalle_pedido,
        name='eliminar_detalle_pedido',
    ),
]
