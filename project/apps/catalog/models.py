from django.db import models
from apps.users.models import customuser as user
from django.core.validators import FileExtensionValidator
class producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='catalog/imagenes/', null=True, blank=True)
    imagen_url = models.URLField(null=True, blank=True)
    categoria = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
class topics_group(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100, default="unknown")
    users_joined = models.ManyToManyField(user,blank=True)
    
    imagen = models.ImageField(upload_to='catalog/group/image', null=True, blank=True)
    imagen_url = models.URLField(null=True, blank=True)
    posts = models.ManyToManyField('post', blank=True)
    score = models.IntegerField(default=0)
    likes = models.ManyToManyField(user, related_name='liked_groups', blank=True)
    dislikes = models.ManyToManyField(user, related_name='disliked_groups', blank=True)
    subscriptions = models.ManyToManyField(user, related_name='subscribed_groups', blank=True)
    def __str__(self):
        return self.nombre

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
    
    
class postimagen(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE, related_name='imagenes', default=None)
    imagen = models.ImageField(upload_to='catalog/post/imagenes/', null=True, blank=True)
    tittle = models.CharField(max_length=200, blank=True, help_text="Optional title for the image")

    def __str__(self):
        return self.tittle or f"Imagen de post {self.post_id}"

class postvideo(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE, related_name='videos', default=None)
    video = models.FileField(upload_to='catalog/post/videos', validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov'])], null=True, blank=True)
    tittle = models.CharField(max_length=200, blank=True, help_text="Optional title for the video")

    def __str__(self):
        return self.tittle or f"Video de post {self.post_id}"