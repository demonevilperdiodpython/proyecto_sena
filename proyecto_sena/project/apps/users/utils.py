
import uuid
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # primera IP en la lista
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip or '127.0.0.1'




def get_device_id(request, response=None):
    device_id = request.COOKIES.get("device_id")
    if not device_id:
        device_id = str(uuid.uuid4())
        if response: # si hay respuesta, guardamos la cookie
            response.set_cookie("device_id", device_id, max_age=60*60*24*365)
    return device_id

import re

def es_gmail_valido(correo):
    patron = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    return re.match(patron, correo) is not None


