from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .models import producto
from .forms import productoForm
from .utils import SepareByClass
from .models import topics_group
from .models import post as post_model
from .forms import postForm
from .forms import topic_groupForm
from apps.users.models import customuser as CustomUser
# Create your views here.



def home(request):
    pecheras = producto.objects.filter(categoria="pechera")
    grupos = SepareByClass(producto)
    grupo = topics_group.objects.all()
    grupo = SepareByClass(topics_group)
    
    best_user  =  CustomUser.objects.order_by('-score')[:10]
    best_group = topics_group.objects.order_by('-score')[:10]
    print(best_user)
    print(grupos)
    return render(request, "catalog/home.html", {"pecheras" :pecheras, "grupos": grupo, "best_users" : best_user, "best_groups": best_group})
#esto esparte de la anterior pagina pero, no es necesario pero no lo quiero borrar
def product_list(request):
    productos = producto.objects.all()

    if request.method == "POST":
        form = productoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:product_list')
    else:
        form = productoForm()

    return render(request, "catalog/product_list.html", {"form": form,"productos": productos})

def eliminate_product(request, product_id):
    product = producto.objects.get(id=product_id)
    product.delete()
    return redirect('catalog:product_list')
#comienza lo creado para el proyecto
def add_group(request):
    if request.method == "POST":
        form = topic_groupForm(request.POST,request.FILES)
        if form.is_valid():
            print('valid')
            form.save()
            return redirect('catalog:home')
        else:
            print('invalid')
    else:
        form = topic_groupForm()
        
    return render(request, "catalog/addGroup.html", {"form": form})



def topic_group(request, id):
    form = postForm(request.POST)
    group= topics_group.objects.get(id=id)
    sections = group.sections.all()
    group_post = group.posts.all()
    
    print(group,group_post)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.group = group
            post.save()
            group.posts.add(post)
            
            
            return redirect('catalog:topic_group', id=id)

    return render(request, "catalog/group.html", {"group": group, "sections": sections, "posts": group_post, "form": form})

def topic_section(request, group_id, section_id):
    group = topics_group.objects.get(id=group_id)
    section = group.sections.get(id=section_id)
    return render(request, "catalog/section.html", {"group": group, "section": section})
def post( request, group_id, section_id):
    group = topics_group.objects.get(id=group_id)
    section = group.sections.get(id=section_id)
    if request.method == "POST":
        content = request.POST.get("content")
        messages.success(request, "Post creado exitosamente.")
        return redirect('catalog:topic_section', group_id=group_id, section_id=section_id)
    return render(request, "catalog/post.html", {"group": group, "section": section})



def eliminate_post(request):
    post_id = request.POST.get("post_id")
    post = post_model.objects.get(id=post_id)
    post.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))
def edit_post(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        Post = post_model.objects.get(id=post_id)
        content = request.POST.get("content")
        Post.content = content
        Post.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))