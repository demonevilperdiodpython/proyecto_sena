from django.apps import AppConfig


class OrdersConfig(AppConfig):
    # Faltaba el atributo 'name', sin el Django no sabe que app es
    # ('apps.orders' must supply a name attribute) y no arranca el servidor.
    name = 'apps.orders'
    default_auto_field = 'django.db.models.BigAutoField'