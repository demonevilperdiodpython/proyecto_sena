
import requests
from django.core.files.base import ContentFile
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from .forms import CustomUserCreationForm as UserForm
from .models import customuser

class CustomSocialAdapter(DefaultSocialAccountAdapter):
    
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        email = data.get('email') or sociallogin.account.extra_data.get('email')
        #muestro  sociallogin.account.extra_data que es el  el archivo json, o lo que contiene (es lo que entiendo)
        #para verificar errores
        print("================================")
        print("PROVIDER:", sociallogin.account.provider)
        print("DATA:", data)
        print("EXTRA DATA:", sociallogin.account.extra_data)
        print("================================")
        #si el hay valor externo de gmail en el auth entonces pone el email en la base de datos 
        if email:
            user.email = email
        return user

    def save_user(self, request, sociallogin, form=None):
        #crea una instancia del usuario puesto en settings, creo que tambien crea uno en la tabla de los registros  usuarios  de google o la respectivo microservicio
        user = super().save_user(request, sociallogin, form)
        extra_data = sociallogin.account.extra_data
        if sociallogin.account.provider == 'google':
            #del json obtengo il item llamado picture 
            avatar_url = sociallogin.account.extra_data.get('picture', '')
        #discord no usa un avatar url, sino una clabe la cual dice cual es el archivo (creo()
        elif sociallogin.account.provider == "discord":
            discord_id = extra_data.get("id")
            avatar_hash = extra_data.get("avatar")
            if discord_id and avatar_hash:
                # Discord puede tener avatares animados
                #revisa que tipo de extencion deberia  tener el archivo
                #no estoy totalmente seguro como funciona, seguramente los nombre de los archivos guardados de discord comienzan por una letra, cada tipo diferente, lo mas posible
                if avatar_hash.startswith("a_"):
                    extension = "gif"
                else:
                    extension = "png"
                #se accede a la imagen dada por discod de esta manera. crea la url y luego la obtiene con get
                
                avatar_url = f"https://cdn.discordapp.com/avatars/{discord_id}/{avatar_hash}.{extension}?size=256"
        elif sociallogin.account.provider == "github":
            avatar_url = sociallogin.account.extra_data.get("avatar_url", "")
                    
        if avatar_url:
            try:
                response = requests.get(avatar_url, timeout=5)
                if response.status_code == 200:
                    file_name = f"google_avatar_{user.id}.jpg"
                    user.imagen.save(file_name, ContentFile(response.content), save=True)
            except Exception as e:
                print("no funciona", e)
        
        
        return user
    def pre_social_login(self, request, sociallogin):
        #en esta funcion no obtengo el usuario ya que esta funcion se utiliza cuando ya hay usuario, pero se hace casi que exactamente lo mismo que antes 
        provider = sociallogin.account.provider
        extra_data = sociallogin.account.extra_data

        if provider == "discord":
            discord_id = extra_data.get("id")
            avatar_hash = extra_data.get("avatar")

            if discord_id and avatar_hash:
                if avatar_hash.startswith("a_"):
                    extension = "gif"
                else:
                    "png"

                avatar_url = f"https://cdn.discordapp.com/avatars/{discord_id}/{avatar_hash}.{extension}?size=256"

                user = sociallogin.user

                if user.pk:
                    
                    try:
                        response = requests.get(avatar_url, timeout=5)
                        #revisa si si se tiene la imagien y todo fue correcto
                        if response.status_code == 200:
                            file_name = f"discord_avatar_{user.id}.{extension}"
                            #guardo el archivo en  la base de datos
                            user.imagen.save(
                                file_name,
                                ContentFile(response.content),
                                save=True
                            )

                    except Exception as e:
                        print("no actauliza:", e)
        elif provider == 'github':
            user = sociallogin.user
            avatar_url = sociallogin.account.extra_data.get("avatar_url", "")
            if avatar_url:
                try:
                    response = requests.get(avatar_url, timeout=5)
                    if response.status_code == 200:
                        file_name = f"github_avatar_{user.id}.jpg"
                        user.imagen.save(file_name, ContentFile(response.content), save=True)
                except Exception as e:
                    print("no funciona", e)
        elif provider == 'google':
                    user = sociallogin.user
                    avatar_url = sociallogin.account.extra_data.get("avatar_url", "")
                    if avatar_url:
                        try:
                            response = requests.get(avatar_url, timeout=5)
                            if response.status_code == 200:
                                file_name = f"google_avatar_{user.id}.jpg"
                                user.imagen.save(file_name, ContentFile(response.content), save=True)
                        except Exception as e:
                            print("no funciona", e)
