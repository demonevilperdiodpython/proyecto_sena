from .common import *
from .auth import para_registrarse
from .ai import group_contexto_ia, doc_como_argumento, preguntar_a_la_ia
from apps.users.permissions import es_moderador_global

@sin_cuenta_no_se_puede_actuar
def add_group(request):
    if request.method == "POST":
        form = topic_groupForm(request.POST, request.FILES)
        if form.is_valid():
            grupo = form.save()
            grupo.creator.add(request.user)
            messages.success(request, "Grupo creado.")
            return redirect('catalog:home')
    else:
        form = topic_groupForm()
    return render(request, "catalog/add_group.html", {"form": form})  # nombre consistente (snake_case)

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

def topic_group(request, id):
    form = postForm(request.POST or None, request.FILES or None)
    group = get_object_or_404(topics_group, id=id)
    group_post = group.post.filter(parent__isnull=True).order_by('-created_at')
    

    puede_admin = group.puede_administrar(request.user)
    es_admin_global = es_moderador_global(request.user)
    esta_baneado = (
        request.user.is_authenticated
        and group.banned_users.filter(id=request.user.id).exists()
    )
    puede_hablar = not esta_baneado

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return para_registrarse(request)
        if esta_baneado:
            messages.error(request, "Estás suspendido en este grupo. Puedes leer, pero no publicar ni comentar.")
            return redirect('catalog:topic_group', id=id)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.group = group  
            parent_id = request.POST.get("parent_id")
            if parent_id:
                try:
                    post.parent = group.post.get(id=parent_id, parent__isnull=True)
                except group.post.model.DoesNotExist:
                    messages.error(request, "Comentario padre inválido")
                    return redirect('catalog:topic_group', id=id)

            post.save()

            if request.POST.get("ia") == "on":
                group = get_object_or_404(topics_group, id=id)

                contexto = group_contexto_ia(group=group)
                doc_text = doc_como_argumento(request, group)
                contexto = contexto + "\n\n  (contenido de archivos .docx del grupo):\n" + doc_text
                respuesta_ia, error_ia, _chat_messages = preguntar_a_la_ia(
                    request, post.content,contexto=contexto, guardar_historial=False)
                if error_ia:
                    messages.warning(request, error_ia)
                else:
                    post_ia = post_model(parent=None, user=None,
                                        content=respuesta_ia, group=group, es_ia=True)
                    post_ia.save()
                    post.ia_response = post_ia
                    post.save()
            guardar_archivos(post, archivos_del_request(request))
    posts = group.post.filter(parent__isnull=True).order_by('-created_at')
    return render(request, "catalog/group.html", {
        'posts': posts,
        'form': form,
        'group': group,
        'group_post': group_post,
        'sections': group.sections.all(),
        'puede_admin': puede_admin,
        'puede_hablar': puede_hablar,
        'es_admin_global': es_admin_global,
        'todos_los_usuarios': (
            CustomUser.objects.order_by('username')
            if es_admin_global
            else CustomUser.objects.none()
        ),
    })



@sin_cuenta_no_se_puede_actuar
def group_admin(request, group_id, user_id):
    """Da o quita admin de un grupo a un usuario suscrito."""
    group = get_object_or_404(topics_group, id=group_id)

    if not group.puede_administrar(request.user):
        messages.error(request, "No tienes permiso para administrar este grupo.")
        return redirect('catalog:topic_group', id=group_id)

    if request.method != "POST":
        return redirect('catalog:topic_group', id=group_id)

    usuario = get_object_or_404(CustomUser, id=user_id)

    if request.POST.get("action") == "remove":
        if (
            group.admin_users.filter(id=usuario.id).exists()
            and not group.creator.exists()
            and group.admin_users.count() <= 1
        ):
            messages.error(
                request,
                "El grupo quedaría sin administradores. Asigna otro admin o un creador primero.",
            )
            return redirect('catalog:topic_group', id=group_id)
        group.admin_users.remove(usuario)
        messages.success(request, f"{usuario.username} ya no es admin del grupo.")
        return redirect('catalog:topic_group', id=group_id)

    if not group.subscriptions.filter(id=user_id).exists():
        messages.error(request, "Ese usuario no está suscrito al grupo.")
        return redirect('catalog:topic_group', id=group_id)

    if usuario.is_banned or not usuario.is_active:
        messages.error(request, "Ese usuario está suspendido o inactivo y no puede ser admin.")
        return redirect('catalog:topic_group', id=group_id)

    if group.banned_users.filter(id=usuario.id).exists():
        messages.error(request, "Quita el ban del grupo antes de darle admin.")
        return redirect('catalog:topic_group', id=group_id)

    group.admin_users.add(usuario)
    messages.success(request, f"{usuario.username} ahora es admin del grupo.")

    return redirect('catalog:topic_group', id=group_id)


@sin_cuenta_no_se_puede_actuar
def group_ban(request, group_id, user_id):
    """Banea o desbanea a un usuario dentro de un solo grupo."""
    group = get_object_or_404(topics_group, id=group_id)

    if not group.puede_administrar(request.user):
        messages.error(request, "No tienes permiso para administrar este grupo.")
        return redirect('catalog:topic_group', id=group_id)

    if request.method != "POST":
        return redirect('catalog:topic_group', id=group_id)

    usuario = get_object_or_404(CustomUser, id=user_id)

    if usuario.id == request.user.id:
        messages.error(request, "No puedes banear a ti mismo.")
        return redirect('catalog:topic_group', id=group_id)

    if request.POST.get("action") == "unban":
        group.banned_users.remove(usuario)
        messages.success(request, f"{usuario.username} ya puede participar en el grupo.")
        return redirect('catalog:topic_group', id=group_id)

    # Los administradores globales pueden banear a cualquier usuario, aunque
    # no este suscrito o sea creador/admin del grupo.
    if not es_moderador_global(request.user):
        if not group.subscriptions.filter(id=usuario.id).exists():
            messages.error(request, "Solo puedes banear a usuarios suscritos al grupo.")
            return redirect('catalog:topic_group', id=group_id)

        if group.creator.filter(id=usuario.id).exists() or group.admin_users.filter(id=usuario.id).exists():
            messages.error(
                request,
                "No puedes banear al creador ni a un admin del grupo. Quítale el admin primero.",
            )
            return redirect('catalog:topic_group', id=group_id)

    group.banned_users.add(usuario)
    messages.success(
        request,
        f"{usuario.username} queda suspendido en este grupo: puede leer, pero no publicar ni comentar.",
    )
    return redirect('catalog:topic_group', id=group_id)


@sin_cuenta_no_se_puede_actuar
def group_ban_any(request, group_id):
    """Permite a un admin global banear a cualquier usuario del grupo."""
    group = get_object_or_404(topics_group, id=group_id)

    if not es_moderador_global(request.user):
        messages.error(request, "Solo un administrador global puede banear a cualquier usuario.")
        return redirect('catalog:topic_group', id=group_id)

    if request.method != "POST":
        return redirect('catalog:topic_group', id=group_id)

    user_id = request.POST.get("user_id")
    if not user_id:
        messages.error(request, "Selecciona un usuario para banear.")
        return redirect('catalog:topic_group', id=group_id)

    usuario = get_object_or_404(CustomUser, id=user_id)

    if usuario.id == request.user.id:
        messages.error(request, "No puedes banear a ti mismo.")
        return redirect('catalog:topic_group', id=group_id)

    group.banned_users.add(usuario)
    messages.success(
        request,
        f"{usuario.username} queda suspendido en este grupo: puede leer, pero no publicar ni comentar.",
    )
    return redirect('catalog:topic_group', id=group_id)


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

    return render(request, "catalog/edit_group.html", {  # nombre consistente
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

    return render(request, "catalog/delete_group.html", {"group": group})  # nombre consistente


# ---------------------------------------------------------------------------
# CRUD de secciones
# ---------------------------------------------------------------------------

