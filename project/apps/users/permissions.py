"""Reglas centralizadas de permisos de la aplicacion."""


def es_moderador_global(user):
    """True si el usuario puede moderar cualquier grupo o publicacion."""
    if not user or not getattr(user, "is_authenticated", False):
        return False
    if getattr(user, "is_banned", False):
        return False
    return bool(
        getattr(user, "is_superuser", False)
        or getattr(user, "is_staff", False)
        or getattr(user, "is_platform_admin", False)
    )


def puede_administrar_grupo(user, group):
    """True si el usuario puede administrar ese grupo concreto."""
    if not user or not getattr(user, "is_authenticated", False) or group is None:
        return False
    if getattr(user, "is_banned", False):
        return False
    if es_moderador_global(user):
        return True
    # Un admin o creador baneado del grupo deja de administrarlo hasta que
    # se le quite el ban. Los moderadores globales no se ven afectados.
    if esta_baneado_de_grupo(user, group):
        return False
    # Interruptor de compatibilidad que ya existia en topics_group.
    if getattr(group, "CUALQUIERA_PUEDE_BORRAR", False):
        return True
    if group.creator.filter(id=user.id).exists():
        return True
    if group.admin_users.filter(id=user.id).exists():
        return True
    return False


def esta_baneado_de_grupo(user, group):
    """True si el usuario solo puede leer ese grupo, sin publicar ni comentar."""
    if not user or not getattr(user, "is_authenticated", False) or group is None:
        return False
    return group.banned_users.filter(id=user.id).exists()


def puede_hablar_en_grupo(user, group):
    """True si el usuario puede publicar o comentar en ese grupo."""
    if not user or not getattr(user, "is_authenticated", False) or group is None:
        return False
    return not esta_baneado_de_grupo(user, group)
