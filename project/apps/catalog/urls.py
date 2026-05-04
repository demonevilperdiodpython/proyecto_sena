from django.urls import path


from . import views
from django.conf import settings
from django.urls import include 
app_name = "catalog"
urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('eliminate_product/<int:product_id>/', views.eliminate_product , name='eliminate_product'),
    path('group/<int:id>/', views.topic_group, name='topic_group'),
    path('add_group/', views.add_group, name='add_group'),
    path('eliminate_post/', views.eliminate_post, name='eliminate_post'),
    path('edit_post/', views.edit_post, name='edit_post'),
]

