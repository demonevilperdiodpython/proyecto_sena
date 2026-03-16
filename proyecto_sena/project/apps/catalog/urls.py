from django.urls import path


from . import views
from django.conf import settings
from django.urls import include 
app_name = "catalog"
urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('eliminate_product/<int:product_id>/', views.eliminate_product , name='eliminate_product'),
    
]
