from django import template

from apps.users.permissions import (
    es_moderador_global,
    esta_baneado_de_grupo,
    puede_administrar_grupo,
)


register = template.Library()


@register.filter
def puede_editar_post(post, user):
    """Misma regla que usan eliminate_post y edit_post."""
    if not user or not getattr(user, "is_authenticated", False):
        return False
    if getattr(user, "is_banned", False):
        return False
    if getattr(post, "user_id", None) == getattr(user, "id", None):
        return True
    if es_moderador_global(user):
        return True
    if getattr(post, "group_id", None) and puede_administrar_grupo(user, post.group):
        return True
    # Se conserva el comportamiento actual: las respuestas de IA se pueden
    # moderar desde la interfaz por cualquier usuario autenticado.
    if getattr(post, "es_ia", False):
        return True
    return False


@register.filter
def puede_hablar_en_grupo(post_or_group, user):
    """False si el usuario esta baneado del grupo de ese post."""
    if not user or not getattr(user, "is_authenticated", False):
        # Sin sesion se mantiene el comportamiento anterior: el formulario se
        # muestra y el POST redirige al registro.
        return True
    group = getattr(post_or_group, "group", None)
    if group is None and hasattr(post_or_group, "banned_users"):
        group = post_or_group
    if group is None:
        return True
    return not esta_baneado_de_grupo(user, group)
