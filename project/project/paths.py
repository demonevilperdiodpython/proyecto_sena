import os
import uuid

from django.utils import timezone
from django.utils.deconstruct import deconstructible


@deconstructible
class ruta_con_fecha:
    """Genera una ruta de subida organizada por carpeta/fecha/uuid.

    Se usa como ``upload_to`` en los campos de archivo/imagen para que los
    archivos no se acumulen con nombres duplicados (``_aB3xY9z``) y queden
    agrupados por fecha dentro de su carpeta logica.
    """

    def __init__(self, carpeta):
        # Sin barra inicial: la carpeta es relativa a MEDIA_ROOT.
        self.carpeta = carpeta.strip("/")

    def __call__(self, instance, filename):
        extension = os.path.splitext(filename)[1].lower()
        fecha = timezone.now().strftime("%Y/%m/%d")
        return f"{self.carpeta}/{fecha}/{uuid.uuid4().hex[:12]}{extension}"
