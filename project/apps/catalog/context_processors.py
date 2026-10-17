from django.db.models import Count

from .models import post as post_model
from .models import topics_group


def hot_topic(request):
    """Datos de la columna lateral 'Hot Topic' para TODAS las vistas.

    Antes cada vista tenía que pasar top_comments y top_groups a mano, y
    solo lo hacía home: en el resto (post, group, section...) la columna
    salía vacía aunque hubiera contenido. Con esto se inyecta siempre.

    Es barato: son dos consultas con LIMIT y la columna solo se pinta en
    las vistas que extienden catalog/home.html.
    """
    top_comments = comentarios_populares()

    top_groups = topics_group.objects.order_by('-score')[:6]

    return {
        'top_comments': top_comments,
        'top_groups': top_groups,
    }


def comentarios_populares(cantidad=5):
    """Comentarios (respuestas directas a un post), los más comentados.

    Antes el filtro era solo parent__isnull=False, que mezclaba dos cosas:
    un post raiz tiene parent=None, pero tambien lo tiene un post raiz al
    que alguien respondio (su parent es el comentario). Ese filtro, ademas,
    ordenaba por reply_count, asi que terminaba mostrando los comentarios
    SIN respuesta y escondia los que si tenian.

    Aqui se filtran solo los comentarios de primer nivel (los que cuelgan
    de un post raiz) y la popularidad se mide por cuantos comentarios
    recibio, no por respuestas anidadas.
    """
    ids_de_posts = post_model.objects.filter(parent__isnull=True).values('id')

    comentarios = (
        post_model.objects
        .filter(parent_id__in=ids_de_posts, group__isnull=False)
        .annotate(replies=Count('children', distinct=True))
        .order_by('-replies', '-created_at')[:cantidad]
    )

    return comentarios