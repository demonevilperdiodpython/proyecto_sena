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
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect



def ia(request):
    return render(request, "catalog/ia.html")
def home(request):

    posts = post_model.objects.order_by('-created_at')[:10]
    grupos = topics_group.objects.all()
    if request.user.is_authenticated:
        posts = post_model.objects.order_by('-created_at')[:10]
        grupos = topics_group.objects.all()
        return render(request, "catalog/home.html", {"grupos": grupos, "posts": posts}) 

    else:
        pecheras = producto.objects.filter(categoria="pechera")
        
        return render(request, "catalog/home.html", {"pecheras": pecheras, "grupos": grupos, "posts": posts}) 

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
def post( request, group_id, section_id):
    group = topics_group.objects.get(id=group_id)
    section = group.sections.get(id=section_id)
    if request.method == "POST":
        content = request.POST.get("content")
        messages.success(request, "Post creado exitosamente.")
        return redirect('catalog:topic_section', group_id=group_id, section_id=section_id)
    return render(request, "catalog/post.html", {"group": group, "section": section})

def topic_section(request, group_id, section_id):
    group = topics_group.objects.get(id=group_id)
    section = group.sections.get(id=section_id)
    return render(request, "catalog/section.html", {"group": group, "section": section})




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

def search_view(request, page_number):
    print('---------------------------------------------------------------------------------------------------------------')
    page_number = max(1, int(page_number or 1))
    best_group = topics_group.objects.order_by('-score')[:5]
    best_user = CustomUser.objects.order_by('-score')[:5]

    if request.method == "POST":
        query = request.POST.get("search", "")
        if query:
            grupo = topics_group.objects.filter(nombre__icontains=query)
        else:
            grupo = topics_group.objects.all()
    else:
        query = request.GET.get("search", "")
        if query:
            grupo = topics_group.objects.filter(nombre__icontains=query)
        else:
            grupo = topics_group.objects.all()

    comienzo = (page_number - 1) * 2
    limite = comienzo + 2
    grupo = grupo[comienzo:limite]
    print(grupo)
    print("puta")
    return render(
        request,
        "catalog/groups.html",
        {
            "grupos": grupo,
            "best_users": best_user,
            "best_groups": best_group,
            "page1": page_number + 1,
            "page2": page_number - 1,
            "page": page_number,
        },
    )

def search(request):
    query = request.GET.get("search")
    grupos = topics_group.objects.filter(name__icontains=query)
    return redirect(search_view, grupos=grupos)

def rate_group(request):
    print("working")
    group_id = request.GET.get('group_id')
    rate = request.GET.get('rate')
    group = topics_group.objects.get(id=group_id)
    if rate == 'like':
        group.likes.add(request.user)
        group.dislikes.remove(request.user)
    elif rate == 'dislike':
        group.dislikes.add(request.user)
        group.likes.remove(request.user)
    group.save()
    redirect_url = request.META.get('HTTP_REFERER', '/')
    return redirect(redirect_url)

def subscribe(request):
    group_id = request.POST.get('group_id')
    group = topics_group.objects.get(id=group_id)
    page = request.POST.get('page') or 1
    if request.user in group.subscriptions.all():
        group.subscriptions.remove(request.user)
    else:
        group.subscriptions.add(request.user)
    group.save()
    
    return HttpResponseRedirect(reverse_lazy('catalog:search_view', kwargs={'page_number': page}))