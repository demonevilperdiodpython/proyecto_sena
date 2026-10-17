from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import producto
from .models import topics_group
from .models import topic_section
from .models import post as post_model
from .forms import postForm
from .forms import topic_groupForm
from apps.users.models import customuser as CustomUser
from .forms import postImagenForm
from .forms import postVideoForm
from .models import postvideo
from ollama import Client
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator



def home(request):
    # top_comments y top_groups ya no se calculan aqui: los inyecta
    # apps.catalog.context_processors.hot_topic en todas las vistas.
    posts = post_model.objects.filter(parent__isnull=True).order_by('-created_at')[:10]
    grupos = topics_group.objects.all()

    if request.user.is_authenticated:
        query = request.GET.get("search_post") or request.POST.get("search_post") or ""

        if query:
            posts = post_model.objects.filter(content__icontains=query)
            posts = posts.filter(parent__isnull=True)

        return render(request, "catalog/home.html", {
            "grupos": grupos,
            "posts": posts,
        })

    else:
        return render(request, "catalog/home.html", {
            "grupos": grupos,
            "posts": posts,
        })

@login_required
def eliminate_product(request, product_id):
    product = get_object_or_404(producto, id=product_id)
    product.delete()
    # Antes redirigia a 'catalog:product_list', una URL que no existe.
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def add_group(request):
    if request.method == "POST":
        form = topic_groupForm(request.POST,request.FILES)
        if form.is_valid():
            # commit=False para poder poner el usuario antes de guardar.
            grupo = form.save(commit=False)
            grupo.creator = request.user
            grupo.save()
            messages.success(request, "Grupo creado exitosamente.")
            return redirect('catalog:topic_group', id=grupo.id)
    else:
        form = topic_groupForm()

    return render(request, "catalog/addGroup.html", {"form": form})


@login_required
def topic_group(request, id):
    print('--------------------DEBUG---------------------')
    form = postForm(request.POST or None)
    
    group = get_object_or_404(topics_group, id=id)
    sections = group.sections.all()
    group_post = group.post.filter(parent__isnull=True).order_by('-created_at')
    videoform = postVideoForm(request.POST or None, request.FILES or None)
    imagenform = postImagenForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST':
        print('--------------------POST REQUEST---------------------')
        if form.is_valid():
            print('--------------------FORM VALID---------------------')
            print("ia response:", request.POST.get("ia"))
            post = form.save(commit=False)
            post.user = request.user
            post.group = group
            
            parent_id = request.POST.get("parent_id")
            if parent_id:
                post.parent_id = parent_id
                
            post.save()
            
            if request.POST.get("ia") == "on":
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

            if imagenform.is_valid() and imagenform.cleaned_data.get('imagen'):
                imagen = imagenform.save(commit=False)
                imagen.post = post
                imagen.save()

            # Redirect SIEMPRE despues de guardar. Antes solo redirigia cuando
            # NO habia imagen: al subir una se quedaba en el POST y el
            # navegador volvia a enviar el formulario al recargar.
            return redirect('catalog:topic_group', id=id)

        # Si el form no es valido se vuelve a pintar con los errores.
    return render(request, "catalog/group.html", {"group": group, 
                                                "sections": sections,
                                                "posts": group_post,
                                                "form": form,
                                                "videoform": videoform,
                                                "imagenform": imagenform,
                                                # Un template no puede llamar a un
                                                # metodo con argumentos, asi que el
                                                # permiso se resuelve aqui.
                                                "puede_admin": group.puede_administrar(request.user)
                                                })
@login_required
def eliminate_post(request):
    post_id = request.POST.get("post_id")
    post = get_object_or_404(post_model, id=post_id)
    post.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def edit_post(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        
        Post = get_object_or_404(post_model, id=post_id)
        content = request.POST.get("content")
        Post.content = content
        Post.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def ia_response(request):
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


@login_required
def search_view(request):
    best_group = topics_group.objects.order_by('-score')[:5]
    best_user = CustomUser.objects.order_by('-score')[:5]

    query = request.POST.get("search") or request.GET.get("search") or ""

    if query:
        groups = topics_group.objects.filter(nombre__icontains=query)
    else:
        groups = topics_group.objects.all()

    # Sin order_by la paginacion puede repetir o saltarse grupos entre paginas.
    groups = groups.order_by('-score', '-id')

    paginator = Paginator(groups, 2)
    page = request.GET.get("page") or request.POST.get("page") or 1
    obj = paginator.get_page(page)
    return render(
        request,
        "catalog/groups.html",
        {
            "grupos": obj,
            "best_users": best_user,
            "best_groups": best_group,
            "page": obj.number,
            "page1": obj.next_page_number() if obj.has_next() else obj.number,
            "page2": obj.previous_page_number() if obj.has_previous() else obj.number,
            "query": query,
        },
    )


def search_view_post(request):

    query = request.POST.get("search_post") or request.GET.get("search") or ""
    if query:
        posts = post_model.objects.filter(content__icontains=query)
    else:
        posts = post_model.objects.all()

    # El paginador va siempre fuera del if: antes solo existia sin query
    # y con busqueda la vista reventaba con NameError.
    posts = posts.order_by('-created_at')

    paginator = Paginator(posts, 2)
    page = request.GET.get("page") or request.POST.get("page") or 1
    obj = paginator.get_page(page)

    return render(
        request,
        "catalog/groups.html",
        {
            "grupos": obj,
            "best_users": CustomUser.objects.order_by('-score')[:5],
            "best_groups": topics_group.objects.order_by('-score')[:5],
            "page": obj.number,
            "page1": obj.next_page_number() if obj.has_next() else obj.number,
            "page2": obj.previous_page_number() if obj.has_previous() else obj.number,
            "query": query,
        },
    )
@login_required
def rate_group(request):
    group_id = request.GET.get('group_id')
    rate = request.GET.get('rate')
    group = get_object_or_404(topics_group, id=group_id)

    # Dar like otra vez quita el like (toggle), en vez de sumar siempre.
    if rate == 'like':
        if request.user in group.likes.all():
            group.likes.remove(request.user)
        else:
            group.likes.add(request.user)
            group.dislikes.remove(request.user)
    elif rate == 'dislike':
        if request.user in group.dislikes.all():
            group.dislikes.remove(request.user)
        else:
            group.dislikes.add(request.user)
            group.likes.remove(request.user)

    group.recalcular_score()
    redirect_url = request.META.get('HTTP_REFERER', '/')
    return redirect(redirect_url)

@login_required
def subscribe(request):
    group_id = request.POST.get('group_id')
    group = get_object_or_404(topics_group, id=group_id)
    page = request.POST.get('page') or 1

    if request.user in group.subscriptions.all():
        group.subscriptions.remove(request.user)
    else:
        group.subscriptions.add(request.user)

    group.recalcular_score()

    # Antes pedia un kwarg 'page_number' que la URL no tiene -> NoReverseMatch.
    return redirect(f"{reverse('catalog:search_view')}?page={page}")

def obtener_input_video(request):
    if request.method == "GET":
        videoform = postVideoForm()
        return render(request, "catalog/includes/_video_form_input.html", {"videoform": videoform})


# ---------------------------------------------------------------------------
# Vistas agregadas
# ---------------------------------------------------------------------------

@login_required
def settings_view(request):
    # La plantilla catalog/settings.html ya existia pero no tenia URL ni vista.
    return render(request, "catalog/settings.html")


def popular(request):
    # Ranking por score. El score lo recalcula topics_group.recalcular_score()
    # cada vez que alguien da like, dislike o se une al grupo.
    top_groups = topics_group.objects.order_by('-score')[:10]
    top_users = CustomUser.objects.order_by('-score')[:10]
    top_posts = post_model.objects.filter(parent__isnull=True).order_by('-created_at')[:10]

    return render(request, "catalog/popular.html", {
        # nombre propio: top_groups del processor son 6 y se usan en el
        # hot_topic; aqui se necesitan 10 para el ranking de la pagina.
        "ranking_grupos": top_groups,
        "ranking_usuarios": top_users,
        "top_posts": top_posts,
    })


@login_required
def post_detail(request, id):
    # Enlace propio para compartir un post: /post/12/
    post_obj = get_object_or_404(post_model, id=id)
    form = postForm(request.POST or None)
    imagenform = postImagenForm(request.POST or None, request.FILES or None)
    videoform = postVideoForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.user = request.user
            respuesta.group = post_obj.group
            respuesta.parent_id = request.POST.get("parent_id") or post_obj.id
            respuesta.save()

            if imagenform.is_valid() and imagenform.cleaned_data.get('imagen'):
                imagen = imagenform.save(commit=False)
                imagen.post = respuesta
                imagen.save()

            if videoform.is_valid() and videoform.cleaned_data.get('video'):
                video = videoform.save(commit=False)
                video.post = respuesta
                video.save()

            return redirect("catalog:post_detail", id=id)

    return render(request, "catalog/post_detail.html", {
        "post": post_obj,
        "group": post_obj.group,
        "form": form,
        "imagenform": imagenform,
        "videoform": videoform,
    })


def ia_view(request):
    # Pagina propia del asistente. La plantilla catalog/ia.html ya existia
    # pero no tenia ruta, solo se usaba por el htmx que hay en los posts.
    return render(request, "catalog/ia.html")


def topic_section_view(request, group_id, section_id):
    # Las secciones quedaron a medias: el modelo existe pero faltaba la
    # plantilla catalog/section.html y la ruta.
    group = get_object_or_404(topics_group, id=group_id)
    section = get_object_or_404(group.sections, id=section_id)
    sections_posts = section.posts.filter(parent__isnull=True).order_by('-created_at')

    return render(request, "catalog/section.html", {
        "group": group,
        "section": section,
        "sections": group.sections.all(),
        "posts": sections_posts,
        "puede_admin": group.puede_administrar(request.user),
    })


@login_required
def post_in_section(request, group_id, section_id):
    # Publicar directamente dentro de una seccion del grupo.
    group = get_object_or_404(topics_group, id=group_id)
    section = get_object_or_404(group.sections, id=section_id)
    form = postForm(request.POST or None)
    videoform = postVideoForm(request.POST or None, request.FILES or None)
    imagenform = postImagenForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            post_obj = form.save(commit=False)
            post_obj.user = request.user
            post_obj.group = group
            post_obj.save()
            section.posts.add(post_obj)

            if request.POST.get("ia") == "on":
                client = Client()
                output = client.generate(
                    model="tinyllama",
                    prompt=f"answer anything youre told: {post_obj.content}",
                    stream=False,
                    options={
                        "num_predict": 100,
                        "temperature": 0.5,
                    }
                )
                post_obj.ia_response = output["response"]
                post_obj.save()

            if videoform.is_valid() and videoform.cleaned_data.get('video'):
                video = videoform.save(commit=False)
                video.post = post_obj
                video.save()

            if imagenform.is_valid() and imagenform.cleaned_data.get('imagen'):
                imagen = imagenform.save(commit=False)
                imagen.post = post_obj
                imagen.save()

            messages.success(request, "Post creado exitosamente.")
            return redirect("catalog:topic_section", group_id=group_id, section_id=section_id)

    return render(request, "catalog/section_post.html", {
        "group": group,
        "section": section,
        "form": form,
        "videoform": videoform,
        "imagenform": imagenform,
    })


# ---------------------------------------------------------------------------
# CRUD de grupos: editar y eliminar
# ---------------------------------------------------------------------------

@login_required
def edit_group(request, id):
    group = get_object_or_404(topics_group, id=id)

    # grupo.puede_administrar() ya revisa el interruptor CUALQUIERA_PUEDE_BORRAR.
    if not group.puede_administrar(request.user):
        messages.error(request, "No tienes permiso para editar este grupo.")
        return redirect('catalog:topic_group', id=id)

    if request.method == "POST":
        form = topic_groupForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, "Grupo actualizado.")
            return redirect('catalog:topic_group', id=id)
    else:
        form = topic_groupForm(instance=group)

    return render(request, "catalog/editGroup.html", {
        "form": form,
        "group": group,
    })


@login_required
def eliminate_group(request, id):
    group = get_object_or_404(topics_group, id=id)

    if not group.puede_administrar(request.user):
        messages.error(request, "No tienes permiso para eliminar este grupo.")
        return redirect('catalog:topic_group', id=id)

    # Si viene por POST se borra. Por GET solo avisa, para no perder
    # un grupo con publicaciones por un clic accidental.
    if request.method == "POST":
        nombre = group.nombre
        group.delete()
        messages.success(request, f"El grupo '{nombre}' fue eliminado.")
        return redirect('catalog:home')

    return render(request, "catalog/deleteGroup.html", {"group": group})


# ---------------------------------------------------------------------------
# CRUD de secciones
# ---------------------------------------------------------------------------

@login_required
def add_section(request, group_id):
    group = get_object_or_404(topics_group, id=group_id)

    if not group.puede_administrar(request.user):
        messages.error(request, "No tienes permiso para crear secciones en este grupo.")
        return redirect('catalog:topic_group', id=group_id)

    if request.method == "POST":
        nombre = request.POST.get("name", "").strip()
        if nombre:
            topic_section.objects.create(name=nombre, group=group)
            messages.success(request, "Sección creada.")
            return redirect('catalog:topic_group', id=group_id)
    else:
        nombre = ""

    return render(request, "catalog/addSection.html", {
        "group": group,
        "nombre": nombre,
    })


@login_required
def edit_section(request, group_id, section_id):
    group = get_object_or_404(topics_group, id=group_id)
    section = get_object_or_404(group.sections, id=section_id)

    if not group.puede_administrar(request.user):
        messages.error(request, "No tienes permiso para editar esta sección.")
        return redirect('catalog:topic_group', id=group_id)

    if request.method == "POST":
        nombre = request.POST.get("name", "").strip()
        if nombre:
            section.name = nombre
            section.save()
            messages.success(request, "Sección actualizada.")
            return redirect('catalog:topic_section', group_id=group_id, section_id=section_id)
    else:
        nombre = section.name

    return render(request, "catalog/editSection.html", {
        "group": group,
        "section": section,
        "nombre": nombre,
    })


@login_required
def eliminate_section(request, group_id, section_id):
    group = get_object_or_404(topics_group, id=group_id)
    section = get_object_or_404(group.sections, id=section_id)

    if not group.puede_administrar(request.user):
        messages.error(request, "No tienes permiso para eliminar esta sección.")
        return redirect('catalog:topic_group', id=group_id)

    # La sección se borra, pero sus posts NO: quedan en el grupo.
    nombre = section.name
    section.delete()
    messages.success(request, f"La sección '{nombre}' fue eliminada. Sus publicaciones siguen en el grupo.")
    return redirect('catalog:topic_group', id=group_id)