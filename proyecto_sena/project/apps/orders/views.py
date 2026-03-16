from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from apps.catalog.models import producto
from apps.users.models import customuser
from .models import orderList
from .models import orderItem

def product_page(request, product_name,product_id):
    product = producto.objects.get(nombre=product_name, id = product_id)
    print(product)
    if request.method == "GET":
        return render(request, "orders/productpage.html", {"product": product})
    else:
        return render(request, "orders/productpage.html", {"product": product})
    
def add_to_cart(request):

    product_name = request.POST.get("product_name")
    product_id = request.POST.get("product_id")
    if request.user == None or not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to add items to your cart.")
        print(product_name, product_id)
        return redirect('orders:product_page', product_id=product_id ,product_name=product_name)
    else:
        product = producto.objects.get(id=product_id)
        product_name = product.nombre
        quantity = request.POST.get("quantity")
        quantity = int(quantity)
        order = orderItem.objects.create(producto = product, number=quantity)
        order.save()
        orderlist  = orderList.objects.get(user=request.user)
        orderlist.productos.add(product)
        print(orderlist.productos.all())


        return redirect(f'orders:product_page', product_name=product_name, product_id=product_id)
