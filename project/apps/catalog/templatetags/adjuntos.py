"""Tags de plantilla para los adjuntos de los posts."""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

PLANTILLA_INPUT = (
    '<input type="file" name="archivos" multiple class="input-archivos" '
    'style="display:none;" aria-label="Archivos adjuntos">'
)

# Texto fijo, sin datos de quien lo escribe, asi que mark_safe basta.
# (format_html sin argumentos lanza TypeError en Django 6.1.)


@register.simple_tag
def input_archivos():
    """Input de adjuntos del post: multiple y sin accept, para poder marcar
    cuantos archivos se quiera, de cualquier tipo.

    Se pinta a mano y no con un forms.FileField porque ese campo espera un
    archivo suelto (hace data.name) y revienta con la lista que devuelve
    request.FILES.getlist. La vista lee los archivos de ahi directamente.

    Es un tag y no una variable del contexto porque el formulario se
    incluye desde cuatro plantillas que viene de cuatro vistas distintas;
    asi no hay que acordarse de anadirlo en todas."""
    return mark_safe(PLANTILLA_INPUT)