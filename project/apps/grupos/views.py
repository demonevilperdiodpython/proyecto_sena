from django.shortcuts import render


# Create your views here.
from django.shortcuts import render

def categorias(request):
    return render(request, 'grupos/categorias.html')