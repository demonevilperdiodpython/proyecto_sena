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
from .models import postvideo
from .models import postarchivo
from ollama import Client
from ollama import ResponseError
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from functools import wraps
from urllib.parse import urlparse


# Modelo que se le pide a Ollama. Para usar otro, se cambia aqui y ya.
MODELO_IA = "tinyllama"


def preguntar_a_la_ia(texto):
    """Pregunta a Ollama y devuelve (respuesta, error).

    Hay dos formas de que esto falle y son distintas:

    - Ollama no esta corriendo: la libreria lanza ConnectionError.
    - Ollama esta corriendo pero el modelo no esta descargado: lanza
      ResponseError con un texto que dice "try pulling it first".

    Antes cada vista llamaba a client.generate() por su cuenta y sin proteccion,
    asi que publicar con la casilla de IA marcada reventaba con un 500 (el post
    ya habia quedado guardado, pero el usuario veia una pagina de error). Con
    este helper las dos cosas se reportan bien.
    """
    try:
        salida = Client().generate(
            model=MODELO_IA,
            prompt="answer anything youre told: {}".format(texto),
            stream=False,
            options={
                "num_predict": 100,
                "temperature": 0.5,
            }
        )
        return salida["response"], None

    except ConnectionError:
        return None, ("La IA no esta conectada: Ollama no esta corriendo. "
                      "Abrir otra terminal y ejecutar 'ollama serve'.")

    except ResponseError:
        return None, ("La IA no tiene el modelo '{}' descargado. "
                      "Ejecutar 'ollama pull {}' para bajarlo.".format(
                          MODELO_IA, MODELO_IA))

    except Exception as error:
        # Cualquier otra cosa (modelo ocupado, sin memoria, timeout) tambien
        # se avisa en vez de tumbar la pagina.
        print("Ollama fallo:", error)
        return None, "La IA no pudo responder en este momento."


def para_registrarse(request):
    """Manda al formulario de REGISTRO, no al de iniciar sesion.

    Se usa en vez de login_required porque al visitante que no tiene
    cuenta lo que le falta es crearla, no iniciar sesion."""
    return redirect(reverse('users:singup') + '?next=' + request.get_full_path())


def sin_cuenta_no_se_puede_actuar(view):
    """Deja VER la pagina sin iniciar sesion, pero para hacer falta una cuenta.

    Con GET (o HEAD) la vista se ejecuta siempre: cualquiera puede navegar
    por toda la aplicacion sin registrarse. Lo que cambia algo (publicar,
    crear grupo, editar, borrar, votar...) necesita sesion, y si no la hay
    se manda al formulario de registro.

    Antes estas vistas llevaban @sin_cuenta_no_se_puede_actuar, que mandaba al login incluso
    para solo mirar la pagina."""
    @wraps(view)
    def envoltura(request, *args, **kwargs):
        if request.method in ('GET', 'HEAD') or request.user.is_authenticated:
            return view(request, *args, **kwargs)
        messages.info(request, 'Registrate para poder publicar y crear grupos.')
        return para_registrarse(request)
    return envoltura


def guardar_archivos(post_obj, archivos):
    """Guarda los adjuntos del post y devuelve cuantos se guardaron.

    Acepta cualquier tipo de archivo y todos los que se marquen a la vez.
    Antes habia dos bloques, uno para video y otro para imagen, y cada uno
    aceptaba un solo archivo."""
    guardados = 0
    for archivo in archivos:
        # Los vacios (0 bytes) se saltan: no son un archivo util.
        if not archivo or not getattr(archivo, 'size', 0):
            continue
        adjunto = postarchivo(post=post_obj)
        adjunto.archivo = archivo
        # Se guarda el nombre que subio el usuario para que al descargar
        # no aparezca el nombre aleatorio del servidor.
        adjunto.nombre_original = getattr(archivo, 'name', '')[:255]
        adjunto.save()
        guardados += 1
    return guardados


def archivos_del_request(request):
    """Los adjuntos que(se subiieron en este POST.

    Se leen de request.FILES y no de un forms.FileField porque ese campo
    espera un archivo suelto y revienta con la lista de getlist."""
    return request.FILES.getlist('archivos')



def posts_del_feed(vista, usuario):
    """Las publicaciones del feed segun la vista pedida.

    Reddit ofrece Hot / New / Top, que es tres formas de ordenar por
    popularidad. Aqui se ofrece otra cosa: lo que necesita ayuda ya. Un post
    sin respuestas y mas viejo es justo lo que deberia verse primero, y en
    una semana de parciales eso vale mas que el post mas reciente.
    """
    base = post_model.objects.filter(parent__isnull=True)

    if vista == 'populares':
        return base.order_by('-score', '-created_at')[:15]

    if vista == 'ayuda':
        # children__isnull: nadie le ha respondido. De mas antiguo a mas
        # nuevo, asi lo que mas lleva esperando queda arriba.
        return base.filter(children__isnull=True).order_by('created_at')[:10]

    if vista == 'mis_grupos' and usuario.is_authenticated:
        # Los grupos donde soy dueno o estoy suscrito.
        mios = topics_group.objects.filter(
            Q(creator=usuario) | Q(subscriptions=usuario))
        return base.filter(group__in=mios).order_by('-created_at')[:10]

    # 'recientes' es la vista normal: lo ultimo publicado, como estaba.
    return base.order_by('-created_at')[:10]


def home(request):
    # top_comments y top_groups ya no se calculan aqui: los inyecta
    # apps.catalog.context_processors.hot_topic en todas las vistas.
    grupos = topics_group.objects.all()

    # Que se esta viendo. Se lee de la URL (?ver=ayuda) para que la vista
    # se pueda compartir y para que el buscador del navegador funcione.
    vista = request.GET.get("ver") or "recientes"
    if vista not in ("recientes", "ayuda", "mis_grupos"):
        vista = "recientes"

    if request.user.is_authenticated:
        query = request.GET.get("search_post") or request.POST.get("search_post") or ""

        if query:
            posts = post_model.objects.filter(content__icontains=query)
            posts = posts.filter(parent__isnull=True)
        else:
            posts = posts_del_feed(vista, request.user)

        return render(request, "catalog/home.html", {
            "grupos": grupos,
            "posts": posts,
            "vista": vista,
            # "Mis grupos" solo tiene sentido con sesion iniciada.
            "puede_ver_mis_grupos": True,
        })

    else:
        posts = posts_del_feed(vista, request.user)
        return render(request, "catalog/home.html", {
            "grupos": grupos,
            "posts": posts,
            # Sin sesion no hay grupos propios, asi que se cae a "recientes".
            "vista": vista if vista != "mis_grupos" else "recientes",
            "puede_ver_mis_grupos": False,
        })

@sin_cuenta_no_se_puede_actuar
def eliminate_product(request, product_id):
    product = get_object_or_404(producto, id=product_id)
    product.delete()
    # Antes redirigia a 'catalog:product_list', una URL que no existe.
    return redirect(request.META.get('HTTP_REFERER', '/'))

@sin_cuenta_no_se_puede_actuar
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
            messages.error(request, "Por favor corrige los errores del formulario para crear el grupo.")
    else:
        form = topic_groupForm()

    return render(request, "catalog/addGroup.html", {"form": form})


def topic_group(request, id):
    # Se puede VER el grupo sin entrar. Para publicar (que es la parte POST)
    # hay que iniciar sesion, y eso se comprueba mas abajo.
    print('--------------------DEBUG---------------------')
    form = postForm(request.POST or None)
    
    group = get_object_or_404(topics_group, id=id)
    sections = group.sections.all()
    group_post = group.post.filter(parent__isnull=True).order_by('-created_at')
    
    if request.method == 'POST':
        # Red de seguridad: el decorador ya manda al registro a quien no
        # tiene cuenta, pero si se llegara aqui con un usuario anonimo
        # fallaria la clave foranea al guardar el post.
        if not request.user.is_authenticated:
            return para_registrarse(request)
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
                respuesta_ia, error_ia = preguntar_a_la_ia(post.content)
                if error_ia:
                    # El post ya quedo guardado; solo faltó la respuesta de la
                    # IA. Se avisa y se sigue como si nada.
                    messages.warning(request, error_ia)
                else:
                    post.ia_response = respuesta_ia
                    post.save()
                    print("output:", respuesta_ia)

            guardar_archivos(post, archivos_del_request(request))

            # Redirect SIEMPRES despues de guardar. Antes solo redirigia cuando
            # NO habia imagen: al subir una se quedaba en el POST y el
            # navegador volvia a enviar el formulario al recargar.
            return redirect('catalog:topic_group', id=id)
        else:
            messages.error(request, "No se pudo publicar. El contenido del post no puede estar vacío.")

        # Si el form no es valido se vuelve a pintar con los errores.
    return render(request, "catalog/group.html", {"group": group, 
                                                "sections": sections,
                                                "posts": group_post,
                                                "form": form,
                                                # Un template no puede llamar a un
                                                # metodo con argumentos, asi que el
                                                # permiso se resuelve aqui.
                                                "puede_admin": group.puede_administrar(request.user)
                                                })
@sin_cuenta_no_se_puede_actuar
def eliminate_post(request):
    post_id = request.POST.get("post_id")
    post = get_object_or_404(post_model, id=post_id)
    post.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@sin_cuenta_no_se_puede_actuar
def edit_post(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        Post = get_object_or_404(post_model, id=post_id)
        content = request.POST.get("content", "").strip()
        if content:
            Post.content = content
            Post.save()
            messages.success(request, "Publicación actualizada.")
        else:
            messages.error(request, "El contenido de la publicación no puede estar vacío.")
    return redirect(request.META.get('HTTP_REFERER', '/'))

def ia_response(request):
    # Antes, si se llegaba con GET (o sin "input_text") la vista se acababa
    # sin return y Django respondia con un error 500. Ahora se vuelve a la
    # pagina de la IA, que es lo que toca.
    if request.method != "POST" or not request.POST.get("input_text", "").strip():
        messages.error(request, "Por favor escribe una pregunta para el asistente.")
        return redirect('catalog:ia')

    print("-------------------------    -------------------------")
    description = request.POST.get("input_text")
    print(description)
    response, error = preguntar_a_la_ia(description)

    if error:
        print("Ollama no respondio:", error)
        return render(request, "catalog/ia_response.html", {"error": error})

    return render(request, "catalog/ia_response.html", {
        "response": response,
        "description": description,
    })


def search_view(request):
    # Buscar y ver los grupos es publico: no hace falta iniciar sesion.
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
            # Sin esto el formulario de responder sale sin caja de texto.
            "form": postForm(),
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
            # Sin esto el formulario de responder sale sin caja de texto.
            "form": postForm(),
        },
    )
@sin_cuenta_no_se_puede_actuar
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

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        return JsonResponse({
            'success': True,
            'id': group.id,
            'score': group.score,
            'likes': group.likes.count(),
            'dislikes': group.dislikes.count(),
            'liked': request.user in group.likes.all(),
            'disliked': request.user in group.dislikes.all(),
        })

    redirect_url = request.META.get('HTTP_REFERER', '/')
    return redirect(redirect_url)


@sin_cuenta_no_se_puede_actuar
def rate_post(request):
    post_id = request.GET.get('post_id')
    rate = request.GET.get('rate')
    p = get_object_or_404(post_model, id=post_id)

    if rate == 'like':
        if request.user in p.likes.all():
            p.likes.remove(request.user)
        else:
            p.likes.add(request.user)
            p.dislikes.remove(request.user)
    elif rate == 'dislike':
        if request.user in p.dislikes.all():
            p.dislikes.remove(request.user)
        else:
            p.dislikes.add(request.user)
            p.likes.remove(request.user)

    p.recalcular_score()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        return JsonResponse({
            'success': True,
            'id': p.id,
            'score': p.score,
            'likes': p.likes.count(),
            'dislikes': p.dislikes.count(),
            'liked': request.user in p.likes.all(),
            'disliked': request.user in p.dislikes.all(),
        })

    redirect_url = request.META.get('HTTP_REFERER', '/')
    return redirect(redirect_url)

@sin_cuenta_no_se_puede_actuar
def subscribe(request):
    group_id = request.POST.get('group_id')
    group = get_object_or_404(topics_group, id=group_id)
    page = request.POST.get('page') or 1

    if request.user in group.subscriptions.all():
        group.subscriptions.remove(request.user)
    else:
        group.subscriptions.add(request.user)

    group.recalcular_score()

    # Si viene con referer y no con page, o si vino desde un grupo:
    redirect_url = request.META.get('HTTP_REFERER')
    if redirect_url and 'group' in redirect_url:
        return redirect(redirect_url)

    # Antes pedia un kwarg 'page_number' que la URL no tiene -> NoReverseMatch.
    return redirect(f"{reverse('catalog:search_view')}?page={page}")

def obtener_input_video(request):
    """Ya no hace falta: el boton de adjuntar es uno solo y no usa htmx.

    Antes este endpoint existia solo para que el boton de video trajera su
    input con hx-get. Se deja la vista para no romper enlaces viejos, pero
    devuelve el formulario de archivos nuevo."""
    return render(request, "catalog/includes/_post_form_card.html", {})


# ---------------------------------------------------------------------------
# Vistas agregadas
# ---------------------------------------------------------------------------

@sin_cuenta_no_se_puede_actuar
def settings_view(request):
    # La plantilla catalog/settings.html ya existia pero no tenia URL ni vista.
    return render(request, "catalog/settings.html")


def popular(request):
    # Ranking por score. El score lo recalcula topics_group.recalcular_score()
    # cada vez que alguien da like, dislike o se une al grupo.
    top_groups = topics_group.objects.order_by('-score', '-id')[:10]
    top_users = CustomUser.objects.order_by('-score', '-id')[:10]
    top_posts = post_model.objects.filter(parent__isnull=True).order_by('-score', '-created_at')[:10]

    return render(request, "catalog/popular.html", {
        # nombre propio: top_groups del processor son 6 y se usan en el
        # hot_topic; aqui se necesitan 10 para el ranking de la pagina.
        "ranking_grupos": top_groups,
        "ranking_usuarios": top_users,
        "top_posts": top_posts,
        # Igual que en la seccion: sin "form" el formulario de responder sale
        # sin caja de texto y no se puede escribir.
        "form": postForm(),
    })


def post_detail(request, id):
    # El post se puede LEER sin entrar. Para responder hace falta sesion.
    # Enlace propio para compartir un post: /post/12/
    post_obj = get_object_or_404(post_model, id=id)
    form = postForm(request.POST or None)

    if request.method == "POST":
        # Red de seguridad, igual que en topic_group.
        if not request.user.is_authenticated:
            return para_registrarse(request)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.user = request.user
            respuesta.group = post_obj.group
            respuesta.parent_id = request.POST.get("parent_id") or post_obj.id
            respuesta.save()

            guardar_archivos(respuesta, archivos_del_request(request))
            messages.success(request, "Respuesta enviada exitosamente.")

            # El formulario de responder se envia aqui desde cualquier pagina
            # (grupo, seccion, popular, explorar). Antes de esto se guardaba y
            # te mandaba a la pagina del post; ahora se vuelve a la pagina de
            # la que venias, que es donde estabas escribiendo.
            return redirect(a_volver(request, "catalog:post_detail", id=id))
        else:
            messages.error(request, "No se pudo enviar la respuesta. El contenido no puede estar vacío.")

    return render(request, "catalog/post_detail.html", {
        "post": post_obj,
        "group": post_obj.group,
        "form": form,
    })


def ia_view(request):
    # Pagina propia del asistente. La plantilla catalog/ia.html ya existia
    # pero no tenia ruta, solo se usaba por el htmx que hay en los posts.
    return render(request, "catalog/ia.html")


def a_volver(request, nombre_url, **kwargs):
    """A donde volver despues de guardar.

    Si el navegador manda Referer y esa pagina es del propio proyecto, se
    vuelve ahi: asi el que responde desde una seccion o desde popular se
    queda donde estaba, en vez de que lo boten a la pagina del post.

    El Referer se revisa antes de usarlo: si alguien fabricara uno que
    apunte a otro sitio, redirigir alli seria un.redirect abierto. Solo se
    acepta si es una ruta interna que empieza por "/".
    """
    anterior = request.META.get("HTTP_REFERER", "")

    if anterior:
        partes = urlparse(anterior)
        # misma pagina: con path vacio, todo es la raiz
        es_del_proyecto = partes.netloc in ("", request.get_host())
        # se rechazan "//sitio.com" (protocolo relativo), que es el truco
        # clasico del redirect abierto
        no_relativo = not partes.path.startswith("//")
        if es_del_proyecto and no_relativo:
            return partes.path + (("?" + partes.query) if partes.query else "")

    return reverse(nombre_url, kwargs=kwargs)


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
        # Sin esto el formulario de responder salia sin caja de texto: la
        # plantilla la pinta con {% for field in form %}, y si la vista no
        # manda "form" no hay nada que iterate y no se podia escribir nada.
        "form": postForm(),
        "puede_admin": group.puede_administrar(request.user),
    })


@sin_cuenta_no_se_puede_actuar
def post_in_section(request, group_id, section_id):
    # Publicar directamente dentro de una seccion del grupo.
    group = get_object_or_404(topics_group, id=group_id)
    section = get_object_or_404(group.sections, id=section_id)
    form = postForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            post_obj = form.save(commit=False)
            post_obj.user = request.user
            post_obj.group = group
            post_obj.save()
            section.posts.add(post_obj)

            if request.POST.get("ia") == "on":
                respuesta_ia, error_ia = preguntar_a_la_ia(post_obj.content)
                if error_ia:
                    messages.warning(request, error_ia)
                else:
                    post_obj.ia_response = respuesta_ia
                    post_obj.save()

            guardar_archivos(post_obj, archivos_del_request(request))

            messages.success(request, "Post creado exitosamente.")
            return redirect("catalog:topic_section", group_id=group_id, section_id=section_id)
        else:
            messages.error(request, "No se pudo crear la publicación. El contenido no puede estar vacío.")

    return render(request, "catalog/section_post.html", {
        "group": group,
        "section": section,
        "form": form,
    })


# ---------------------------------------------------------------------------
# CRUD de grupos: editar y eliminar
# ---------------------------------------------------------------------------

@sin_cuenta_no_se_puede_actuar
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
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = topic_groupForm(instance=group)

    return render(request, "catalog/editGroup.html", {
        "form": form,
        "group": group,
    })


@sin_cuenta_no_se_puede_actuar
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

@sin_cuenta_no_se_puede_actuar
def add_section(request, group_id):
    group = get_object_or_404(topics_group, id=group_id)

    if not group.puede_administrar(request.user):
        messages.error(request, "No tienes permiso para crear secciones en este grupo.")
        return redirect('catalog:topic_group', id=group_id)

    error = None
    if request.method == "POST":
        nombre = request.POST.get("name", "").strip()
        if nombre:
            topic_section.objects.create(name=nombre, group=group)
            messages.success(request, "Sección creada exitosamente.")
            return redirect('catalog:topic_group', id=group_id)
        else:
            error = "El nombre de la sección no puede estar vacío."
            messages.error(request, error)
    else:
        nombre = ""

    return render(request, "catalog/addSection.html", {
        "group": group,
        "nombre": nombre,
        "error": error,
    })


@sin_cuenta_no_se_puede_actuar
def edit_section(request, group_id, section_id):
    group = get_object_or_404(topics_group, id=group_id)
    section = get_object_or_404(group.sections, id=section_id)

    if not group.puede_administrar(request.user):
        messages.error(request, "No tienes permiso para editar esta sección.")
        return redirect('catalog:topic_group', id=group_id)

    error = None
    if request.method == "POST":
        nombre = request.POST.get("name", "").strip()
        if nombre:
            section.name = nombre
            section.save()
            messages.success(request, "Sección actualizada exitosamente.")
            return redirect('catalog:topic_section', group_id=group_id, section_id=section_id)
        else:
            error = "El nombre de la sección no puede estar vacío."
            messages.error(request, error)
    else:
        nombre = section.name

    return render(request, "catalog/editSection.html", {
        "group": group,
        "section": section,
        "nombre": nombre,
        "error": error,
    })


@sin_cuenta_no_se_puede_actuar
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