from django.shortcuts import render

from .forms import CustomAuthenticationForm as AuthenticationForm
from django.shortcuts import redirect
from django.contrib.auth import login
from .utils import get_client_ip, get_device_id, es_gmail_valido
from .models import UserSession
from .models import customuser as User
from .forms import CustomUserCreationForm as UserCreationForm
import re
from django.contrib.auth import logout
from apps.catalog.models import post
from apps.users.models import imagen as ImagenModel
# Create your views here.cu
def login_view(request):
    form = AuthenticationForm(request)
    response = render(request, 'users/login.html', {"form": form})
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
       
        if form.is_valid():
            ip = get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT','')
            user = form.get_user()
            other_users = UserSession.objects.filter(user=user, is_active=True).update(is_active=False)

            response = redirect('catalog:home')
            device_id = get_device_id(request, response)
            init_sesion = UserSession.objects.create(
                user=user,
                ip_address=ip,
                user_agent=user_agent,
                device_id=device_id)
            init_sesion.save()
            login(request, user)
            return response
            
    return response



def Register_view(request):
    form = UserCreationForm()
    imagen = ImagenModel.objects.all()
    response = render(request, 'users/register.html', {"imagen":imagen,"form": form})
    
    print('register ----------------------------------------------------------------------------------------------------------------------')   
    if request.method == 'POST':
        print('POST request received in Register_view')
        form = UserCreationForm(request.POST, request.FILES)
        
        print(form.data, form.is_valid())
        if form.is_valid():
            print('----------form is valid-----------')
            
            if es_gmail_valido(form.cleaned_data['email']):
                pass
            else:
                return render(request, 'users/register.html',  {"form" : form, "error" : "gmail no valido"})
            
            ip = get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT','')
            device_id = get_device_id(request, response)

            other_users = UserSession.objects.filter(ip_address=ip,
                                            user_agent=user_agent,
                                            device_id=device_id).update(is_active=False)
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
            other_users = UserSession.objects.filter(user=user, is_active=True).update(is_active=False)
            init_sesion = UserSession.objects.create(
                device_id = device_id,
                user=user,
                ip_address=ip,
                user_agent= user_agent)
            init_sesion.save()
            login(request, user)
            return response
        else:
            print('----------form is invalid-----------')
            print(form.errors)
    return response

def acounts_view(request):
    if request.method == 'GET': 
        device_id = request.COOKIES.get("device_id")
        ip= get_client_ip(request)
        user_agent= request.META.get('HTTP_USER_AGENT','')
        userssessions = UserSession.objects.filter(ip_address = ip, user_agent= user_agent, device_id=device_id, is_active=True)
        response = render(request, 'users/acounts.html', {"ingresed_users": userssessions})
        return response

def perfil_view(request, id):
    posts = post.objects.filter(user=request.user)

    return render(request, "users/perfil.html", {
        "posts": posts,
    })



def logOut_view(request):
    ip = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    device_id = request.COOKIES.get("device_id")
    
    print(f"DEBUG Logout: ip={ip}, user_agent={user_agent}, device_id={device_id}, user={request.user}")
    
    if request.user.is_authenticated:
        queryset = UserSession.objects.filter(user=request.user, is_active=True)
        if device_id:
            queryset = queryset.filter(device_id=device_id)
        print(f"DEBUG: Sessions found before update: {list(queryset.values('id', 'is_active'))}")
        updated = queryset.update(is_active=False)
        print(f"DEBUG: Sessions updated: {updated}")
        queryset_after = UserSession.objects.filter(user=request.user, is_active=True)
        print(f"DEBUG: Sessions after update: {list(queryset_after.values('id', 'is_active'))}")
    else:
        print("DEBUG: Logout requested without authenticated user")
    
    logout(request)
    response = redirect('users:login')
    response.delete_cookie('device_id')
    return response

def eliminate_user_session_view(request, user_id):
    if request.method == 'POST':
        response = redirect('users:acounts')
        ip = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        device_id = request.COOKIES.get("device_id")
        
        user = UserSession.objects.filter(user=request.user, user_id=user_id, is_active=True).first()
        if user.user_id == request.user.id:
            logout(request)
            
           
            
            user.is_active = False
            user.save()
        else:
            user.is_active = False
            user.save()
        return response
def log_in_with_user_view(request):
    username = request.GET.get('user')
    if request.method == 'POST':
        username = request.POST.get('user')
        print(username)
        data = request.POST.copy()
        data['username'] = username
        form = AuthenticationForm(request, data=data, user=username)  # Agregar user=username
        if form.is_valid():
            response = redirect('users:acounts')
            device_id = get_device_id(request, response)
            user_agent = request.META.get('HTTP_USER_AGENT','')
            ip = get_client_ip(request)
            
            UserSessionn = UserSession.objects.get(user=form.get_user(), ip_address=ip, user_agent=user_agent, device_id=device_id)
            UserSessionn.is_active = True
            UserSessionn.save()
            user = form.get_user()
            login(request, user)
            
            return response
        
        return render(request, 'users/loginwith.html', {"form": form, "username": username})
    else:
        form = AuthenticationForm(request, user=username)  # Ya estaba correcto aquí
        return render(request, 'users/loginwith.html', {"form": form, "username": username})