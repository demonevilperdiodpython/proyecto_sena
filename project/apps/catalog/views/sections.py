from .common import *
from .ai import group_contexto_ia, preguntar_a_la_ia


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

# --- Detalle de grupo, secciones y posts ---

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
                contexto = group_contexto_ia(group)
                respuesta_ia, error_ia, _chat_messages = preguntar_a_la_ia(
                    request, post_obj.content, contexto=contexto, guardar_historial=False)
                if error_ia:
                    messages.warning(request, error_ia)
                else:
                    post_ia = post_model(parent=None, user=None, content=respuesta_ia, group=post_obj.group)
                    post_ia.save()
                    post_obj.ia_response = post_ia
                    post_obj.save()

            guardar_archivos(post_obj, archivos_del_request(request))
            messages.success(request, "Post creado exitosamente.")

    return render(request, "catalog/section_post.html", {
        "group": group,
        "section": section,
        "form": form,
    })


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

    return render(request, "catalog/add_section.html", {  # nombre consistente
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

    return render(request, "catalog/edit_section.html", {  # nombre consistente
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

