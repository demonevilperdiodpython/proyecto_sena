from django.shortcuts import render
from django.shortcuts import render
from apps.catalog.models import topics_group
from apps.catalog.utils import SepareByClass

def categorias(request):
    grupos = SepareByClass(topics_group)

    return render(
        request,
        "grupos/categorias.html",
        {"grupos": grupos}
    )

# Create your views here.
