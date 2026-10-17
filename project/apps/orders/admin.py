from django.contrib import admin

from .models import orderlist, orderlistdetalle


@admin.register(orderlist)
class orderlistAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'fecha', 'total')


@admin.register(orderlistdetalle)
class orderlistdetalleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'orderlist', 'producto', 'cantidad')
