import os
import uuid
import mimetypes

from django.db import models
from apps.users.models import customuser as user
from django.core.validators import FileExtensionValidator
from django.utils import timezone


def ruta_con_fecha(carpeta):
    """Genera 'carpeta/2026/10/12/nombre-aleatorio.jpg'.

    Django no sobreescribe: si el archivo ya existe le pega un sufijo
   ('_aB3xY9z'), y como el campo nunca se limpia, cada reintento dejaba
    una copia nueva. Con un nombre aleatorio cada subida es un archivo
    unico y las subdirectorios por fecha evitan meter miles de archivos
    en una sola carpeta.
    """
    def subir(instance, filename):
        extension = os.path.splitext(filename)[1].lower()
        fecha = timezone.now().strftime("%Y/%m/%d")
        return f"{carpeta}/{fecha}/{uuid.uuid4().hex[:12]}{extension}"
    return subir


class producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to=ruta_con_fecha('catalog/productos'), null=True, blank=True)
    imagen_url = models.URLField(null=True, blank=True)
    categoria = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
class topics_group(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default="")
    categoria = models.CharField(max_length=100, default="unknown")
    users_joined = models.ManyToManyField(user,blank=True)

    # Dueño del grupo. Si es None, el grupo es viejo (creado antes de
    # este campo) y cualquiera con permiso puede administrarlo.
    creator = models.ForeignKey(user, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_groups')
    
    imagen = models.ImageField(upload_to=ruta_con_fecha('catalog/grupos'), null=True, blank=True)
    imagen_url = models.URLField(null=True, blank=True)
    score = models.IntegerField(default=0)
    likes = models.ManyToManyField(user, related_name='liked_groups', blank=True)
    dislikes = models.ManyToManyField(user, related_name='disliked_groups', blank=True)
    subscriptions = models.ManyToManyField(user, related_name='subscribed_groups', blank=True)
    def __str__(self):
        return self.nombre

    def recalcular_score(self):
        # Cada like suma 1, cada dislike resta 1, y unirse al grupo suma 2.
        # Asi el score siempre refleja el estado real sin desajustarse.
        self.score = self.likes.count() - self.dislikes.count() + (self.subscriptions.count() * 2)
        self.save()
        return self.score

    # Si lo pones en False, solo el dueño (o un superusuario) puede
    # editar y borrar grupos. En True, cualquier usuario logueado puede.
    CUALQUIERA_PUEDE_BORRAR = True

    def puede_administrar(self, usuario):
        if not usuario.is_authenticated:
            return False
        if usuario.is_superuser:
            return True
        if self.CUALQUIERA_PUEDE_BORRAR:
            return True
        # Grupo sin dueño (creado antes de este campo): se permite.
        return self.creator_id is None or self.creator_id == usuario.id

class topic_section(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(topics_group, on_delete=models.CASCADE, related_name='sections')
    posts = models.ManyToManyField('post', blank=True)
    def __str__(self):
        return self.name

class post(models.Model):
    content = models.TextField(max_length=1000)
    user = models.ForeignKey(user, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add= True)
    group = models.ForeignKey('topics_group', on_delete=models.CASCADE, related_name='post', blank = True, null=True)
    ia_response= models.TextField(blank=True, null=True)
    
    parent = models.ForeignKey('self',null=True,on_delete=models.CASCADE, blank=True, related_name="children")
    
    
class postimagen(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE, related_name='imagenes', default=None)
    imagen = models.ImageField(upload_to=ruta_con_fecha('catalog/post/imagenes'), null=True, blank=True)
    tittle = models.CharField(max_length=200, blank=True, help_text="Optional title for the image")
    
    def __str__(self):
        return self.tittle or f"Imagen de post {self.post_id}"

class postvideo(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE, related_name='videos', default=None)
    video = models.FileField(upload_to=ruta_con_fecha('catalog/post/videos'), validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov'])], null=True, blank=True)
    tittle = models.CharField(max_length=200, blank=True, help_text="Optional title for the video")

    def __str__(self):
        return self.tittle or f"Video de post {self.post_id}"


class postarchivo(models.Model):
    """Un archivo adjunto a un post: el que sea, de cualquier tipo.

    Antes habia dos modelos, postimagen (solo imagenes) y postvideo (mp4,
    avi, mov) y dos botones. Ahora hay uno solo y se pueden subir varios a
    la vez. Los dos modelos viejos se conservan para que los posts que ya
    tienen imagen o video sigan mostrandolos."""

    post = models.ForeignKey(post, on_delete=models.CASCADE, related_name='archivos')
    # FileField y no ImageField: asi acepta cualquier tipo de archivo.
    archivo = models.FileField(upload_to=ruta_con_fecha('catalog/post/archivos'))
    # Nombre original, para que se vea al descargar y no el del servidor.
    nombre_original = models.CharField(max_length=255, blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_original or self.archivo.name.rsplit('/', 1)[-1]

    @property
    def nombre(self):
        """Nombre con el que se muestra y se descarga."""
        return self.nombre_original or self.archivo.name.rsplit('/', 1)[-1]

    @property
    def tipo(self):
        """'imagen', 'video', 'audio' o 'otro'.

        Lo deducimos de la extension, no del tipo MIME que mando el
        navegador: el campo FileField guarda solo la ruta."""
        extension = self.archivo.name.rsplit('.', 1)[-1].lower() if '.' in self.archivo.name else ''
        tipo_mime = mimetypes.guess_type('x.' + extension)[0] or ''
        if tipo_mime.startswith('image/'):
            return 'imagen'
        if tipo_mime.startswith('video/'):
            return 'video'
        if tipo_mime.startswith('audio/'):
            return 'audio'
        return 'otro'

    @property
    def peso_legible(self):
        """'1,4 MB'. El archivo puede no estar en disco todavia."""
        try:
            peso = self.archivo.size
        except (OSError, ValueError):
            return ''
        if peso < 1024:
            return '{} B'.format(peso)
        if peso < 1024 * 1024:
            return '{:.0f} KB'.format(peso / 1024)
        if peso < 1024 * 1024 * 1024:
            return '{:.1f} MB'.format(peso / (1024 * 1024))
        return '{:.1f} GB'.format(peso / (1024 * 1024 * 1024))