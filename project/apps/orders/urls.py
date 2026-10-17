from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('nuevo/', views.crear_pedido, name='crear_pedido'),
    path('<int:pk>/agregar/', views.agregar_producto_pedido, name='agregar_producto_pedido'),
    path(
        '<int:pedido_pk>/detalle/<int:pk>/eliminar/',
        views.eliminar_detalle_pedido,
        name='eliminar_detalle_pedido',
    ),
]
