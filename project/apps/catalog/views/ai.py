from .common import *
from ..ai_code import (
    doc_como_argumento,
    _get_historial,
    _guardar_historial,
    _contexto_ia,
    group_contexto_ia,
    preguntar_a_la_ia,
)


def ia_view(request):
    if request.method == "POST":
        form = postForm(request.POST, request.FILES)
        if form.is_valid():
            contexto = None
            if request.user.is_authenticated:
                contexto = _contexto_ia(request.user)
            #utilizo commit false para poder asignar el usuario y el grupo antes de guardar el post
            nuevo_post = form.save(commit=False)
            nuevo_post.user = request.user
            nuevo_post.group = None
            nuevo_post.save()
            #guardo los tres valores que me da la funcion para luego utilizarlos
            # OJO: el tercer valor es la lista de mensajes del chat, NO el
            # modulo django.contrib.messages. Se renombra para no pisarlo.
            respuesta, error, _chat_messages = preguntar_a_la_ia(
                request, nuevo_post.content, contexto=contexto, guardar_historial=True)
            if error:
                messages.warning(request, error)
            else:
                post_ia = post_model(parent=None, user=None, content=respuesta, group=None, es_ia=True)
                post_ia.save()
                nuevo_post.ia_response = post_ia
                nuevo_post.save()
                messages.success(request, "Publicación enviada.")

            guardar_archivos(nuevo_post, archivos_del_request(request))
            return redirect('catalog:ia')
        else:
            messages.error(request, "No se pudo publicar. El contenido no puede estar vacío.")

    # En /ia solo se muestran las preguntas del usuario en sesion y las
    # respuestas de IA asociadas a ellas (no las de otros usuarios).
    if request.user.is_authenticated:
        mis_preguntas = post_model.objects.filter(
            user=request.user, group__isnull=True, es_ia=False)
    else:
        mis_preguntas = post_model.objects.filter(
            user__isnull=True, group__isnull=True, es_ia=False)
 
    ids_preguntas = list(mis_preguntas.values_list('id', flat=True))
    ids_ia = list(mis_preguntas.exclude(ia_response__isnull=True).values_list('ia_response', flat=True))
    posts = post_model.objects.filter(
        id__in=ids_preguntas + ids_ia).order_by('-created_at')[:50]
    form = postForm()
    return render(request, "catalog/ia.html", {"form": form, "posts": posts})



def ia_api_view(request):
    if request.method == "POST":
        host = (request.POST.get("ia_host") or "").strip()
        key = (request.POST.get("ia_api_key") or "").strip()
        if host:
            request.session["ia_host"] = host
        if key:
            request.session["ia_api_key"] = key
        request.session.modified = True

    return render(request, "catalog/includes/ia_api.html", {
        "ia_host": request.session.get("ia_host", ""),
        "ia_api_key": request.session.get("ia_api_key", ""),
    })
def ia_response(request):
    if request.method == "POST":
        texto = request.POST.get("input_text", "").strip()
        respuesta, error, _chat_messages = preguntar_a_la_ia(request, texto)
        historial = _get_historial(request)
        return render(request, "catalog/ia_response.html", {
            "historial": historial, "error": error,
        })
    historial = _get_historial(request)
    return render(request, "catalog/ia_response.html", {"historial": historial})

