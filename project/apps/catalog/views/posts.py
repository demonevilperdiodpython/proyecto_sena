from .common import *
from .auth import para_registrarse
from apps.users.permissions import (
    es_moderador_global,
    esta_baneado_de_grupo,
    puede_administrar_grupo,
)


@sin_cuenta_no_se_puede_actuar
def eliminate_post(request):
    post_id = request.POST.get("post_id")
    post = get_object_or_404(post_model, id=post_id)

    es_autor = request.user == post.user
    es_moderador = es_moderador_global(request.user)
    es_admin_grupo = bool(post.group) and puede_administrar_grupo(request.user, post.group)

    if not (es_autor or es_moderador or es_admin_grupo):
        messages.error(request, "No tienes permiso para eliminar esta publicación.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    post.delete()
    messages.success(request, "Publicación eliminada.")
    return redirect(request.META.get('HTTP_REFERER', '/'))


@sin_cuenta_no_se_puede_actuar
def edit_post(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        Post = get_object_or_404(post_model, id=post_id)

        es_autor = request.user == Post.user
        es_moderador = es_moderador_global(request.user)
        es_admin_grupo = bool(Post.group) and puede_administrar_grupo(request.user, Post.group)

        if not (es_autor or es_moderador or es_admin_grupo):
            messages.error(request, "No tienes permiso para editar esta publicación.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        if (
            Post.group
            and esta_baneado_de_grupo(request.user, Post.group)
            and not es_moderador
            and not es_admin_grupo
        ):
            messages.error(request, "Estás suspendido en este grupo y no puedes editar publicaciones.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        content = request.POST.get("content", "").strip()
        if content:
            Post.content = content
            Post.save()
            messages.success(request, "Publicación actualizada.")
        else:
            messages.error(request, "El contenido de la publicación no puede estar vacío.")
    return redirect(request.META.get('HTTP_REFERER', '/'))



# --- Busqueda ---



def post_detail(request, id):
    # El post se puede LEER sin entrar. Para responder hace falta sesion.
    # Enlace propio para compartir un post: /post/12/
    post_obj = get_object_or_404(post_model, id=id)
    form = postForm(request.POST or None)
    esta_baneado = (
        request.user.is_authenticated
        and post_obj.group
        and post_obj.group.banned_users.filter(id=request.user.id).exists()
    )
    puede_hablar = not esta_baneado

    if request.method == "POST":
        # Red de seguridad, igual que en topic_group.
        if not request.user.is_authenticated:
            return para_registrarse(request)
        if esta_baneado:
            messages.error(request, "Estás suspendido en este grupo y no puedes responder.")
            return redirect(a_volver(request, "catalog:post_detail", id=id))
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
        "puede_hablar": puede_hablar,
    })





# Helper movido a apps.catalog.utils (a_volver).



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

