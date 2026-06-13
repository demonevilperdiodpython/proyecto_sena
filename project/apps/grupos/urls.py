from django.urls import path
from . import views

app_name = "grupos"

urlpatterns = [
    path('', views.categorias, name='categorias'),

]


