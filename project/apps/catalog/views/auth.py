from .common import *

def para_registrarse(request):
    """Manda al formulario de REGISTRO, no al de iniciar sesion.

    Se usa en vez de login_required porque al visitante que no tiene
    cuenta lo que le falta es crearla, no iniciar sesion."""
    return redirect(reverse('users:singup') + '?next=' + request.get_full_path())


# Decorador movido a apps.catalog.utils (sin_cuenta_no_se_puede_actuar).


# Helpers movidos a apps.catalog.utils (guardar_archivos, archivos_del_request,
# posts_del_feed para mantener esta vista mas manejable.

