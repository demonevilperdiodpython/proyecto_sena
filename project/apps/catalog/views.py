from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import producto
from .forms import productoForm
from .utils import SepareByClass
from .models import topics_group
from .models import post as post_model
from .forms import postForm
from .forms import topic_groupForm
from apps.users.models import customuser as CustomUser
from .forms import postImagenForm
from .forms import postVideoForm
from .models import postvideo
from ollama import Client

def ia(request):
    return render(request, "catalog/ia.html")
def home(request):
    pecheras = producto.objects.filter(categoria="pechera")
    grupos = SepareByClass(producto)
    grupo = topics_group.objects.all()
    grupo = SepareByClass(topics_group)
    
    best_user  =  CustomUser.objects.order_by('-score')[:5]
    best_group = topics_group.objects.order_by('-score')[:5]
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
    print('--------------------DEBUG---------------------')
    form = postForm(request.POST or None)
    group = topics_group.objects.get(id=id)
    sections = group.sections.all()
    group_post = group.post.all()
    videoform = postVideoForm(request.POST or None, request.FILES or None)
    imagenform = postImagenForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST':
        print('--------------------POST REQUEST---------------------')
        if form.is_valid():
            print('--------------------FORM VALID---------------------')
            print(request.POST.get("ia"))
            post = form.save(commit=False)
            post.user = request.user
            post.group = group
            post.save()
            if request.POST.get("ia") == "True":
                print('--------------------IA REQUEST---------------------')
                client = Client()
                output = client.generate(
                    model="tinyllama",
                    prompt=f"answer anything youre told: {post.content}",
                    stream=False,
                    options={
                        "num_predict": 100,
                        "temperature": 0.5,
                    }
                )
                print("output:", output["response"])
                post.ia_response = output["response"]
                post.save()
            if videoform.is_valid() and videoform.cleaned_data.get('video'):
                video = videoform.save(commit=False)
                video.post = post
                video.save()
            else:
                print('videoform errors:', videoform.errors)

            if imagenform.is_valid() and imagenform.cleaned_data.get('imagen'):
                imagen = imagenform.save(commit=False)
                imagen.post = post
                imagen.save()
            else:
                print('imagenform errors:', imagenform.errors)
                return redirect('catalog:topic_group', id=id)
            
            print(request.method == 'POST' and request.POST.get("ia") == "True")
        

    return render(request, "catalog/group.html", {"group": group, 
                                                "sections": sections,
                                                "posts": group_post,
                                                "form": form,
                                                "videoform": videoform,
                                                "imagenform": imagenform
                                                })
                                                #"postvideos": post_video,
                                                #"postimagen": post_imagen,
                                                
                                                
                                                #"imagen_form": imagen_form})

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

def ia_response(request):
        # Support htmx/htmlx detection without requiring middleware
  
    
    if request.method == "POST" and request.POST.get("input_text"):
        print("-------------------------    -------------------------")
        description = request.POST.get("input_text")
        print(description)
        client = Client()
        output = client.generate(
            model="tinyllama",
            prompt=f"answer anything youre told: {description}",
            stream=False,
            options={
                "num_predict": 100,
                "temperature": 0.5,
            }
        )
        context={
            "response": output["response"],
            "description": description}
        return render(request, "catalog/ia_response.html", context=context)

def groups_list(request):
    pecheras = producto.objects.filter(categoria="pechera")
    grupos = SepareByClass(producto)
    grupo = topics_group.objects.all()
    grupo = SepareByClass(topics_group)

    best_group = topics_group.objects.order_by('-score')[:5]
    best_user  =  CustomUser.objects.order_by('-score')[:5]
    return render(request, "catalog/groups.html", {"pecheras" :pecheras, "grupos": grupo, "best_users" : best_user, "best_groups": best_group})

def search(request):
    query = request.GET.get("search")
    grupos = topics_group.objects.filter(name__icontains=query)
    return render(request, "catalog/search_results.html", {"grupos": grupos, "query": query})