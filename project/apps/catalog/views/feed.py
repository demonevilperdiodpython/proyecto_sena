from .common import *

def home(request):
    # top_comments y top_groups ya no se calculan aqui: solo utilizo la funcion
        # apps.catalog.context_processors.hot_topic ahora se utilza en cada vista
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

# Vista no usada eliminada para simplificar el modulo.


# --- Grupos: crear, editar, borrar, puntuar, suscribir ---

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
def settings_view(request):
    # La plantilla catalog/settings.html ya existia pero no tenia URL ni vista.
    return render(request, "catalog/settings.html")


# --- Popular y detalle de post ---

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

