from django.db.models import Q

from .models import post as post_model
from .models import topics_group
from .models import postarchivo


def SepareByClass(set):
    categorias = {}
    Grup = set.objects.all()

    for i in Grup:
        categoria = i.categoria
        if categoria not in categorias:
            categorias[categoria] = [i]
        else:
            categorias[categoria].append(i)
    return categorias


# --- Helpers extraidos de views para mantenerlas manejables ---


def guardar_archivos(post_obj, archivos):
    # Guarda los archivos adjuntos de un post, saltando los vacios.
    guardados = 0
    for archivo in archivos:
        if not archivo or not getattr(archivo, 'size', 0):
            continue
        adjunto = postarchivo(post=post_obj)
        adjunto.archivo = archivo
        adjunto.nombre_original = getattr(archivo, 'name', '')[:255]
        adjunto.save()
        guardados += 1
    return guardados


def archivos_del_request(request):
    return request.FILES.getlist('archivos')


def posts_del_feed(vista, usuario):
    base = post_model.objects.filter(parent__isnull=True)

    if vista == 'populares':
        return base.order_by('-score', '-created_at')[:15]

    if vista == 'ayuda':
        return base.filter(children__isnull=True).order_by('created_at')[:10]

    if vista == 'mis_grupos' and usuario.is_authenticated:
        mios = topics_group.objects.filter(
            Q(creator=usuario) | Q(subscriptions=usuario))
        return base.filter(group__in=mios).order_by('-created_at')[:10]

    return base.order_by('-created_at')[:10]


# --- Decorador y helper de navegacion (extraidos de views) ---

from functools import wraps
from django.contrib import messages
from django.urls import reverse
from urllib.parse import urlparse


def sin_cuenta_no_se_puede_actuar(view):
    # Decorador: si no hay sesion, redirige al registro en vez de fallar.
    @wraps(view)
    def envoltura(request, *args, **kwargs):
        if request.method in ('GET', 'HEAD') or request.user.is_authenticated:
            return view(request, *args, **kwargs)
        messages.info(request, 'Registrate para poder publicar y crear grupos.')
        # Import tardio para evitar importacion circular con views.
        from . import views
        return views.para_registrarse(request)
    return envoltura


def a_volver(request, nombre_url, **kwargs):
    """A donde volver despues de guardar (ver views para detalle)."""
    anterior = request.META.get("HTTP_REFERER", "")

    if anterior:
        partes = urlparse(anterior)
        es_del_proyecto = partes.netloc in ("", request.get_host())
        no_relativo = not partes.path.startswith("//")
        if es_del_proyecto and no_relativo:
            return partes.path + (("?" + partes.query) if partes.query else "")

    return reverse(nombre_url, kwargs=kwargs)