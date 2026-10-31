from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout

from .forms import CustomAuthenticationForm as AuthenticationForm
from .forms import CustomUserCreationForm as UserCreationForm
from .utils import get_client_ip, get_device_id, es_gmail_valido
from .models import UserSession, customuser as User, imagen as ImagenModel
from apps.catalog.models import post

import re  # validacion simple en vistas
# Create your views here.cu
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            ip = get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT','')
            user = form.get_user()
            UserSession.objects.filter(user=user, is_active=True).update(is_active=False)

            response = redirect('catalog:home')
            device_id = get_device_id(request, response)
            init_sesion = UserSession.objects.create(
                user=user,
                ip_address=ip,
                user_agent=user_agent,
                device_id=device_id)
            init_sesion.save()
            login(request, user)
            messages.success(request, f"¡Bienvenido de nuevo, {user.username}!")
            return response
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos. Por favor verifica tus datos.")
    else:
        form = AuthenticationForm(request)
    return render(request, 'users/login.html', {"form": form})



def Register_view(request):
    imagen = ImagenModel.objects.all()
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            if not es_gmail_valido(form.cleaned_data['email']):
                messages.error(request, "El correo electrónico debe ser una cuenta de Gmail válida (@gmail.com).")
                return render(request, 'users/register.html', {"imagen": imagen, "form": form, "error": "El correo debe ser de Gmail (@gmail.com)."})

            ip = get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT','')

            user = form.save(commit=False)
            uploaded_image = form.cleaned_data.get('imagen')
            selected_default = request.POST.get('default_image')

            if uploaded_image:
                user.imagen = uploaded_image
            elif selected_default:
                user.imagen = selected_default
            # If neither is provided, leave the model default image in place.

            user.save()

            response = redirect('catalog:home')
            device_id = get_device_id(request, response)
            UserSession.objects.filter(ip_address=ip, user_agent=user_agent, device_id=device_id).update(is_active=False)
            UserSession.objects.filter(user=user, is_active=True).update(is_active=False)
            init_sesion = UserSession.objects.create(
                device_id=device_id,
                user=user,
                ip_address=ip,
                user_agent=user_agent)
            init_sesion.save()
            login(request, user)
            messages.success(request, f"¡Cuenta creada con éxito! Bienvenido, {user.username}.")
            return response
        else:
            messages.error(request, "Por favor corrige los errores señalados en el formulario de registro.")
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {"imagen": imagen, "form": form})

def acounts_view(request):
    # DESHABILITADA a pedido. Esta pagina no la lista de usuarios: es la de
    # las SESIONES ABIERTAS, y filtra por la misma IP + navegador + equipo, o
    # sea que theoretically solo mostraba cuentas abiertas en este mismo
    # dispositivo.
    #
    # No se borra ni la vista ni la plantilla (users/accounts.html): se deja
    # el codigo ahi y solo se impide entrar. Para volver a habilitarla:
    # 1) quitar el return de abajo,
    # 2) devolver los enlaces del navbar y del menu lateral
    #    (templates/plantilla.html y apps/catalog/templates/
    #     catalog/includes/_sidebar.html).
    messages.info(request, "La pagina de sesiones quedo deshabilitada.")
    return redirect('catalog:home')

def perfil_view(request, id):
    # Antes ignoraba el id y siempre mostraba el perfil de quien visita.
    # Ahora /acounts/perfil/5/ muestra el perfil del usuario 5.
    perfil = get_object_or_404(User, id=id)

    posts = post.objects.filter(user=perfil, parent__isnull=True).order_by('-created_at')

    paginator = Paginator(posts, 5)
    numero_pagina = request.GET.get('page')
    page_obj = paginator.get_page(numero_pagina)
    contexto = {
        'page_obj': page_obj,
        'posts': posts,
        'perfil': perfil,
        'es_propio': request.user == perfil,
    }

    # Cambiar la foto y editar el perfil solo tiene sentido en el perfil propio.
    if request.method == "POST" and perfil == request.user:
        if request.FILES.get("cambio_foto"):
            perfil.imagen = request.FILES["cambio_foto"]
            perfil.save()
            messages.success(request, "Foto de perfil actualizada exitosamente.")
        else:
            messages.warning(request, "No seleccionaste ninguna imagen para cambiar.")
        return redirect("users:Perfil", id=perfil.id)

    return render(request, "users/perfil.html", contexto)



def logOut_view(request):
    ip = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    device_id = request.COOKIES.get("device_id")
    
    # Debug prints eliminados para mantener la salida limpia.
    if request.user.is_authenticated:
        queryset = UserSession.objects.filter(user=request.user, is_active=True)
        if device_id:
            queryset = queryset.filter(device_id=device_id)
        queryset.update(is_active=False)
    
    logout(request)
    response = redirect('users:login')
    response.delete_cookie('device_id')
    return response

def eliminate_user_session_view(request, user_id):
    # Sin sesion no hay nada que cerrar: antes la consulta devolvia None y
    # la linea siguiente reventaba con AttributeError (error 500).
    if not request.user.is_authenticated:
        return redirect('users:acounts')

    if request.method == 'POST':
        response = redirect('users:acounts')
        ip = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        device_id = request.COOKIES.get("device_id")

        user = UserSession.objects.filter(user_id=user_id, is_active=True).first()
        # La sesion puede no existir (o ya estar cerrada): antes eso daba
        # error 500 al usar None.
        if user is not None:
            # Si la sesion que se cierra es la de este mismo dispositivo,
            # ademas se cierra la sesion de django.
            if user.user_id == request.user.id:
                logout(request)
            user.is_active = False
            user.save()
        return response
    return redirect('users:acounts')
def log_in_with_user_view(request):
    # DESHABILITADA a pedido.
    #
    # Esta vista iniciaba sesion como la cuenta que se le pidiera, SIN
    # preguntar la contrasena: armaba el AuthenticationForm solo con el
    # nombre y, si era valido, hacia login. O sea que un POST a
    # /acounts/loginwith con "user=laura" entraba como Laura. No es un
    # forgot de una cuenta: es entrar a cualquier cuenta.
    #
    # Antes solo se llegaba desde la pagina de sesiones, que ademas exigia
    # tener abierta la cuenta en ese mismo dispositivo; esa pagina ya quedo
    # deshabilitada. Aqui se cierra tambien la ruta, que si no se quedaba
    # viva con solo saber la direccion.
    #
    # No se borra la vista ni su URL, pero el codigo que hacia el login se
    #Alejandro al final de este archivo, en log_in_with_user_view_original(),
    # para poder recuperarlo. Si se rehabilita, hay que pedir ademas la
    # contrasena del usuario.
    messages.info(request, "La entrada con otra cuenta quedo deshabilitada.")
    return redirect('catalog:home')


def log_in_with_user_view_original(request):
    """Codigo de la entrada con otra cuenta. NO SE USA.

    Esta es la version que estaba antes de deshabilitarla. Se conserva aqui
    como referencia. OJO: tal como esta, deja entrar sin contrasena, asi que
    no volver a conectarla sin arreglarlo antes.
    """
    username = request.GET.get('user')
    if request.method == 'POST':
        username = request.POST.get('user')
        # print eliminado
        data = request.POST.copy()
        data['username'] = username
        form = AuthenticationForm(request, data=data, user=username)  # Agregar user=username
        if form.is_valid():
            response = redirect('users:acounts')
            device_id = get_device_id(request, response)
            user_agent = request.META.get('HTTP_USER_AGENT','')
            ip = get_client_ip(request)
            
            # .get() lanzaba DoesNotExist (error 500) si esa combinacion de
            # ip/navegador/dispositivo no estaba guardada. Con filter().first()
            # simplemente se continua.
            UserSessionn = UserSession.objects.filter(
                user=form.get_user(), ip_address=ip,
                user_agent=user_agent, device_id=device_id).first()
            if UserSessionn is not None:
                UserSessionn.is_active = True
                UserSessionn.save()
            user = form.get_user()
            login(request, user)
            
            return response
        
        return render(request, 'users/loginwith.html', {"form": form, "username": username})
    else:
        form = AuthenticationForm(request, user=username)  # Ya estaba correcto aquí
        return render(request, 'users/loginwith.html', {"form": form, "username": username})
