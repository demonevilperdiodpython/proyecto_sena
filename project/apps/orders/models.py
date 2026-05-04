from django.db import models
from django.conf import settings
from apps.catalog.models import producto
from apps.users.models import customuser
class orderList(models.Model):
    user = models.ForeignKey(customuser, on_delete=models.CASCADE)
    productos = models.ManyToManyField(producto , blank=False)
    def __str__(self):
        return f"orderlist of {self.user.nombre}"
    
    
class orderItem(models.Model):
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    
    number = models.IntegerField(default=1)
    def __str__(self):
        return f"orderItem: {self.producto.nombre}"
    