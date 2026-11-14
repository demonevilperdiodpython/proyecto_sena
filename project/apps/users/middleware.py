from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect


class BanMiddleware:
    """Cierra la sesion de los usuarios suspendidos en cualquier peticion."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if (
            user is not None
            and user.is_authenticated
            and getattr(user, "is_banned", False)
        ):
            logout(request)
            messages.error(
                request,
                "Tu cuenta esta suspendida. Contacta al administrador.",
            )
            return redirect("users:login")
        return self.get_response(request)
