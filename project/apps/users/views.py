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
from  apps.orders.models import orderList
from apps.users.models import imagen as ImagenModel
# Create your views here.cu
def login_view(request):
    form = AuthenticationForm(request)
    response = render(request, 'users/login.html', {"form": form})
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
       
        if form.is_valid():
            ip = get_client_ip(request)
            device_id = get_device_id(request, response)
            user_agent = request.META.get('HTTP_USER_AGENT','')
            user = form.get_user()
            other_users = UserSession.objects.filter(ip_address = ip,
                                                    user_agent= user_agent,
                                                    device_id=device_id).update(is_active=False)

            init_sesion = UserSession.objects.create(
                user=user,
                ip_address=ip,
                user_agent=user_agent,
                device_id=device_id)
            init_sesion.save()
            login(request, user)
            
    return response



def Register_view(request):
    form = UserCreationForm()
    imagen = ImagenModel.objects.all()
    response = render(request, 'users/register.html', {"imagen":imagen,"form": form})
    
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        
        if form.is_valid():
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
            print("TESTOOOOOOOOOO------------------------------------------------------------------------------")
            user = form.save(commit=False)
            if form.cleaned_data['imagen'] == None:
                img = request.POST.get('default_image')
                user.imagen = img
                user = form.save()
            else:
                user = form.save()
                print(form.cleaned_data['imagen'])
            print("TESTOOOOOOOOOO-------------------------------------------------------------------------------")


            init_sesion = UserSession.objects.create(
                device_id = device_id,
                user=user,
                ip_address=ip,
                user_agent= user_agent)
            init_sesion.save()
            OrderList = orderList.objects.create(user=user)
            OrderList.save()

            login(request, user)
            return redirect('catalog:home')
    return response

def acounts_view(request):
    if request.method == 'GET': 
        ip= get_client_ip(request)
        user_agent= request.META.get('HTTP_USER_AGENT','')
        userssessions = UserSession.objects.filter(ip_address = ip, user_agent= user_agent)
        response = render(request, 'users/acounts.html', {"ingresed_users": userssessions})
        return response
    

def logOut_view(request):
    ip = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    device_id = request.COOKIES.get("device_id")
    
    print(f"DEBUG Logout: ip={ip}, user_agent={user_agent}, device_id={device_id}, user={request.user}")
    
    if device_id:
        queryset = UserSession.objects.filter(
            ip_address=ip,
            user_agent=user_agent,
            device_id=device_id,
            user=request.user
        )
        print(f"DEBUG: Sessions found before update: {list(queryset.values('id', 'is_active'))}")
        updated = queryset.update(is_active=False)
        print(f"DEBUG: Sessions updated: {updated}")
        # Verifica después del update
        queryset_after = UserSession.objects.filter(
            ip_address=ip,
            user_agent=user_agent,
            device_id=device_id,
            user=request.user
        )
        print(f"DEBUG: Sessions after update: {list(queryset_after.values('id', 'is_active'))}")
    else:
        print("DEBUG: No device_id in cookies")
    
    logout(request)
    return redirect('users:login')

def eliminate_user_session_view(request, user_id):
    if request.method == 'POST':
        response= redirect('users:acounts')
        ip = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        device_id = request.COOKIES.get("device_id")
        user =UserSession.objects.get(user_id = user_id, user_agent=user_agent, ip_address=ip, device_id=device_id)
        if user.user_id == request.user.id:
            logout(request)
        user.delete()
        
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