
from django.contrib import admin
from django.urls import path
from django.urls import include 
from . import views
app_name = "orders"
urlpatterns = [ 
    path("order/product/<str:product_name>/<int:product_id>/", views.product_page, name="product_page"),
    path("order/add_to_cart/", views.add_to_cart, name="add_to_cart")
]
