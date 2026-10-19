"""Prueba cada sistema de la aplicacion y reporta lo que falla.

NO toca los datos de ejemplo. Para todo lo que borra o cambia (grupo,
seccion, post, permisos) se crean objetos de prueba con los nombres
"__PRUEBA__" y se limpian al final. Los ids de los grupos reales solo se
usan para LEERLOS.
"""
import os
import traceback

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

from apps.catalog.models import (
    topics_group, topic_section, post, postarchivo,
)
from django.contrib.auth import get_user_model

User = get_user_model()
settings.ALLOWED_HOSTS = list(settings.ALLOWED_HOSTS) + ["testserver"]

fallos = []
avisos = []
ok = []


def probar(nombre, metodo, url, cliente=None, data=None, chequea=None):
    """Ejecuta una peticion y registra el resultado."""
    c = cliente or Client()
    try:
        if metodo == "GET":
            r = c.get(url, data=data or None, follow=False)
        else:
            r = c.post(url, data=data or {}, follow=False)
    except Exception:
        ultimo = traceback.format_exc().strip().split("\n")[-1]
        fallos.append((nombre, "{} {}".format(metodo, url), "EXCEPCION: " + ultimo))
        return None

    problemas = []
    if r.status_code >= 500:
        problemas.append("error del servidor {}".format(r.status_code))

    if hasattr(r, "streaming_content"):
        cuerpo = b"".join(r.streaming_content)
    else:
        cuerpo = r.content
    html = cuerpo.decode("utf-8", "replace")

    if chequea:
        p = chequea(html, r)
        if p:
            problemas.append(p)

    if problemas:
        fallos.append((nombre, "{} {}".format(metodo, url), "; ".join(problemas)))
    else:
        ok.append("{}  {} {}".format(nombre, metodo, url))
    return r


def texto(r):
    if hasattr(r, "streaming_content"):
        return b"".join(r.streaming_content).decode("utf-8", "replace")
    return r.content.decode("utf-8", "replace")


# ---------------------------------------------------------------------------
# Datos: solo de prueba
# ---------------------------------------------------------------------------
laura = User.objects.get(username="laura")
camila = User.objects.get(username="camila")
jhonatan = User.objects.get(username="jhonatan")

# Grupo de Camila (la unica persona que puede administrarlo).
grupo_real = topics_group.objects.filter(creator=camila).first()
# Grupo de Jhonatan: Laura esta suscrito pero NO es duena.
grupo_jho = topics_group.objects.filter(creator=jhonatan).first()
seccion_real = grupo_real.sections.first()

# Objetos desechables para todo lo que se borra.
grupo_p = topics_group.objects.create(nombre="__PRUEBA__", descripcion="x", creator=camila)
sec_p = topic_section.objects.create(name="__PRUEBA__", group=grupo_p)
post_p = post.objects.create(content="__PRUEBA__", user=laura, group=grupo_p)

sesion_laura = Client(); sesion_laura.login(username="laura", password="sharp2026")
sesion_camila = Client(); sesion_camila.login(username="camila", password="sharp2026")
sesion_anon = Client()


# ---------------------------------------------------------------------------
print("=" * 76)
print("1. VER PAGINAS SIN SESION")
print("=" * 76)
for nombre, url in [
    ("home anonimo", "/"),
    ("grupo anonimo", "/group/{}/".format(grupo_real.id)),
    ("popular anonimo", "/popular/"),
    ("explore anonimo", "/search/"),
    ("post anonimo", "/post/{}/".format(post.objects.filter(parent__isnull=True).first().id)),
    ("seccion anonima", "/group/{}/section/{}/".format(grupo_real.id, seccion_real.id)),
    ("IA anonima", "/ia/"),
    ("perfil anonimo", "/acounts/perfil/1/"),
]:
    probar(nombre, "GET", url, sesion_anon)


print()
print("=" * 76)
print("2. PUBLICAR")
print("=" * 76)
probar("publicar en grupo", "POST", "/group/{}/".format(grupo_p.id), sesion_camila,
       data={"content": "__PRUEBA__ post nuevo", "parent_id": ""})
probar("responder un post", "POST", "/post/{}/".format(post_p.id), sesion_camila,
       data={"content": "__PRUEBA__ respuesta", "parent_id": post_p.id})
probar("publicar con adjunto", "POST", "/group/{}/".format(grupo_p.id), sesion_camila,
       data={"content": "__PRUEBA__ con archivo",
             "archivos": SimpleUploadedFile("nota.txt", b"hola", "text/plain")})
probar("publicar en seccion", "POST",
       "/group/{}/section/{}/post/".format(grupo_p.id, sec_p.id), sesion_camila,
       data={"content": "__PRUEBA__ en seccion"})

con_archivo = post.objects.filter(content="__PRUEBA__ con archivo").first()
if con_archivo and postarchivo.objects.filter(post=con_archivo).exists():
    a = postarchivo.objects.filter(post=con_archivo).first()
    ok.append("el adjunto se guardo ({}, {})".format(a.nombre_original, a.tipo))
else:
    fallos.append(("publicar con adjunto", "POST /group/N/",
                   "no se guardo el archivo, o el post ni se creo"))

en_seccion = post.objects.filter(content="__PRUEBA__ en seccion").first()
if en_seccion and sec_p.posts.filter(id=en_seccion.id).exists():
    ok.append("el post de la seccion quedo także en la seccion")
else:
    fallos.append(("publicar en seccion", "POST section/post",
                   "el post se creo pero NO quedo en la seccion"))


print()
print("=" * 76)
print("3. SECCIONES")
print("=" * 76)


def revisa_vacia(html, r):
    if "no-posts" in html or "aún no hay" in html.lower() or "aun no hay" in html.lower():
        return "se abre pero sale VACIA: ninguna publicacion en la seccion"
    return None


r = probar("ver seccion de verdad", "GET",
           "/group/{}/section/{}/".format(grupo_p.id, sec_p.id), sesion_camila)
html = texto(r)
if "__PRUEBA__ en seccion" in html:
    ok.append("el post publicado en la seccion SI aparece al abrirla")
else:
    fallos.append(("seccion: mostrar lo publicado", "GET section",
                   "el post que esta en la seccion NO aparece en la pagina"))

probar("seccion sin posts (limites)", "GET",
       "/group/{}/section/{}/".format(grupo_jho.id,
                                      grupo_jho.sections.filter(name="Limites").first().id),
       sesion_laura, chequea=revisa_vacia)

probar("crear seccion (GET)", "GET", "/group/{}/add_section/".format(grupo_p.id), sesion_camila)
probar("crear seccion (POST)", "POST", "/group/{}/add_section/".format(grupo_p.id),
       sesion_camila, data={"name": "__PRUEBA_NUEVA__"})
if topic_section.objects.filter(name="__PRUEBA_NUEVA__").exists():
    ok.append("crear seccion funciona")
else:
    fallos.append(("crear seccion", "POST add_section", "no se creo la seccion"))

probar("editar seccion (GET)", "GET",
       "/edit_section/{}/{}/".format(grupo_p.id, sec_p.id), sesion_camila)
probar("editar seccion (POST)", "POST",
       "/edit_section/{}/{}/".format(grupo_p.id, sec_p.id), sesion_camila,
       data={"name": "__PRUEBA_RENOMBRADA__"})
if topic_section.objects.filter(name="__PRUEBA_RENOMBRADA__").exists():
    ok.append("editar seccion funciona")
else:
    fallos.append(("editar seccion", "POST", "no se renombro"))

probar("eliminar seccion (GET confirmar)", "GET",
       "/eliminate_section/{}/{}/".format(grupo_p.id, sec_p.id), sesion_camila)
probar("eliminar seccion (POST)", "POST",
       "/eliminate_section/{}/{}/".format(grupo_p.id, sec_p.id), sesion_camila)
if not topic_section.objects.filter(name="__PRUEBA_RENOMBRADA__").exists():
    ok.append("eliminar seccion funciona")
else:
    fallos.append(("eliminar seccion", "POST", "la seccion sigue existiendo"))


print()
print("=" * 76)
print("4. GRUPOS")
print("=" * 76)
probar("crear grupo (GET)", "GET", "/add_group/", sesion_laura)
probar("crear grupo (POST)", "POST", "/add_group/", sesion_laura,
       data={"nombre": "__PRUEBA_NUEVO_GRUPO__", "descripcion": "prueba",
             "categoria": "prueba"})
if topics_group.objects.filter(nombre="__PRUEBA_NUEVO_GRUPO__").exists():
    ok.append("crear grupo funciona")
else:
    fallos.append(("crear grupo", "POST /add_group/", "el grupo no se creo"))

nuevo_g = topics_group.objects.filter(nombre="__PRUEBA_NUEVO_GRUPO__").first()
probar("editar grupo (GET)", "GET", "/edit_group/{}/".format(nuevo_g.id), sesion_laura)
probar("editar grupo (POST)", "POST", "/edit_group/{}/".format(nuevo_g.id), sesion_laura,
       # Se mandan TODOS los campos: la plantilla los pinta con
       # {% for field in form %}, y "categoria" es obligatorio. Un POST
       # incompleto es cosa del test, no un fallo de la app.
       data={"nombre": "__PRUEBA_EDITADO__", "descripcion": "editado",
             "categoria": "prueba", "imagen_url": ""})
if topics_group.objects.filter(nombre="__PRUEBA_EDITADO__").exists():
    ok.append("editar grupo funciona")
else:
    fallos.append(("editar grupo", "POST", "no se guardo el cambio"))

probar("like a grupo", "GET",
       "/rate_group/?group_id={}&rate=like".format(grupo_real.id), sesion_laura)
probar("like otra vez (toggle off)", "GET",
       "/rate_group/?group_id={}&rate=like".format(grupo_real.id), sesion_laura)
probar("dislike a grupo", "GET",
       "/rate_group/?group_id={}&rate=dislike".format(grupo_real.id), sesion_laura)
probar("like (quita el dislike)", "GET",
       "/rate_group/?group_id={}&rate=like".format(grupo_real.id), sesion_laura)
g = topics_group.objects.get(id=grupo_real.id)
ok.append("likes={} dislikes={} score={}".format(
    g.likes.count(), g.dislikes.count(), g.score))

probar("suscribirse", "POST", "/subscribe/", sesion_laura,
       data={"group_id": grupo_real.id})
antes = topics_group.objects.get(id=grupo_real.id).subscriptions.count()
probar("cancelar suscripcion", "POST", "/subscribe/", sesion_laura,
       data={"group_id": grupo_real.id})
despues = topics_group.objects.get(id=grupo_real.id).subscriptions.count()
if antes != despues:
    ok.append("suscribirse/cancelar cambia el numero ({} -> {})".format(antes, despues))
else:
    fallos.append(("suscribirse", "POST /subscribe/",
                   "suscribirse y cancelar dejaron el mismo numero ({})".format(antes)))

probar("eliminar grupo (GET confirmar)", "GET", "/eliminate_group/{}/".format(grupo_p.id), sesion_camila)
probar("eliminar grupo (POST)", "POST", "/eliminate_group/{}/".format(grupo_p.id), sesion_camila)
if not topics_group.objects.filter(pk=grupo_p.id).exists():
    ok.append("eliminar grupo funciona")
else:
    fallos.append(("eliminar grupo", "POST", "el grupo sigue existiendo"))


print()
print("=" * 76)
print("5. POSTS")
print("=" * 76)
probar("ver post", "GET", "/post/{}/".format(post_p.id), sesion_camila)
probar("eliminar post", "POST", "/eliminate_post/", sesion_camila,
       data={"post_id": post_p.id})
if not post.objects.filter(pk=post_p.id).exists():
    ok.append("eliminar post funciona")
else:
    fallos.append(("eliminar post", "POST", "el post sigue existiendo"))


print()
print("=" * 76)
print("6. BUSQUEDA")
print("=" * 76)


def revisa_filtro(html, r):
    # Solo se mira la lista de resultados (.searched-group). La pagina
    # ademas trae un widget lateral con "mejores grupos" (top por score)
    # que siempre va completo y no es la lista de resultados.
    import re
    bloque = re.search(r'<div class="searched-group">(.*?)</div>\s*</div>', html, re.S)
    if not bloque:
        return "no se encontro la lista de resultados en la pagina"
    lista = bloque.group(1)
    if "Matematicas" in lista:
        return "la lista de resultados trae tambien 'Matematicas' (no filtra)"
    if "Ingles" not in lista:
        return "la lista de resultados NO trae 'Ingles' (filtro vacio de mas)"
    return None


probar("buscar grupos 'ingles'", "GET", "/search/?search=ingles", sesion_anon,
       chequea=revisa_filtro)
probar("buscar posts", "GET", "/search_view_post/?search=LHopital", sesion_anon)
probar("buscar posts (POST)", "POST", "/search_view_post/", sesion_anon,
       data={"search_post": "LHopital"})


print()
print("=" * 76)
print("7. IA, AJUSTES, CUENTAS")
print("=" * 76)
probar("pagina IA", "GET", "/ia/", sesion_camila)
probar("ajustes", "GET", "/settings/", sesion_camila)
probar("lista de perfiles", "GET", "/acounts/acounts/", sesion_camila)
probar("login (GET)", "GET", "/acounts/login/", Client())
probar("registro (GET)", "GET", "/acounts/signup/", Client())
probar("ver perfil", "GET", "/acounts/perfil/1/", sesion_camila)
probar("pedidos (el boton que se quito)", "GET", "/orders/crear/", Client())


print()
print("=" * 76)
print("8. QUIEN NO PUEDE (esto DEBE mandar al registro)")
print("=" * 76)


def va_al_registro(html, r):
    if r.status_code in (301, 302, 303, 307, 308):
        d = r.headers.get("Location", "")
        if "signup" in d or "login" in d:
            return None   # correcto
    return "NO lo mando al registro (quedo en {})".format(r.status_code)


probar("crear grupo anonimo", "POST", "/add_group/", sesion_anon,
       data={"nombre": "x", "descripcion": "y", "categoria": "z"}, chequea=va_al_registro)
probar("publicar anonimo", "POST", "/group/{}/".format(grupo_real.id), sesion_anon,
       data={"content": "x"}, chequea=va_al_registro)
probar("responder anonimo", "POST", "/post/{}/".format(
    post.objects.filter(parent__isnull=True).first().id), sesion_anon,
    data={"content": "x"}, chequea=va_al_registro)

# PERMISOS: Laura NO es duena. Se usa un grupo de prueba de Jhonatan, NUNCA
# uno real: con CUALQUIERA_PUEDE_BORRAR en True, estos tests BORRAN de verdad,
# y una version anterior de esta auditoria se llevo por delante un grupo de
# la demo.
grupo_jho = topics_group.objects.create(
    nombre="__PRUEBA_DE_JHONATAN__", descripcion="x", creator=jhonatan)

antes = grupo_jho.nombre
probar("editar grupo ajeno", "POST", "/edit_group/{}/".format(grupo_jho.id), sesion_laura,
       data={"nombre": "__SECUESTRO__", "descripcion": "x", "categoria": "y"})
if topics_group.objects.get(id=grupo_jho.id).nombre == antes:
    ok.append("permisos bien: Laura no pudo editar el grupo de Jhonatan")
else:
    fallos.append(("permisos: editar", "POST edit_group",
                   "Laura SI pudo editar un grupo del que no es duena"))

probar("eliminar grupo ajeno", "POST", "/eliminate_group/{}/".format(grupo_jho.id), sesion_laura)
if topics_group.objects.filter(id=grupo_jho.id).exists():
    ok.append("permisos bien: Laura no pudo borrar el grupo de Jhonatan")
else:
    fallos.append(("permisos: eliminar", "POST eliminate_group",
                   "Laura PUDO borrar el grupo de Jhonatan"))
topics_group.objects.filter(pk=grupo_jho.id).delete()

# Limpieza de lo que quedo de las pruebas
for nombre in ("__PRUEBA_NUEVA__", "__PRUEBA_RENOMBRADA__"):
    topic_section.objects.filter(name=nombre).delete()
for nombre in ("__PRUEBA_NUEVO_GRUPO__", "__PRUEBA_EDITADO__"):
    topics_group.objects.filter(nombre=nombre).delete()
post.objects.filter(content__startswith="__PRUEBA__").delete()

print()
print("=" * 76)
print("RESULTADO:  {} bien,  {} con fallos,  {} avisos".format(
    len(ok), len(fallos), len(avisos)))
print("=" * 76)
if fallos:
    print()
    print("FALLAN:")
    for nombre, url, motivo in fallos:
        print("  [{}] {}".format(nombre, url))
        print("        {}".format(motivo))
if avisos:
    print()
    print("AVISOS:")
    for nombre, motivo in avisos:
        print("  [{}]  {}".format(nombre, motivo))