from django.db import models

# Create your models here.
class producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    imagen_url = models.URLField(null=True, blank=True)
    categoria = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

