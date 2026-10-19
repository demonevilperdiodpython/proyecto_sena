"""Crea los datos de ejemplo: 4 personas, 3 grupos y las conversaciones.

Solo para la base de datos nueva. Se puede borrar este archivo cuando ya
no se necesite.
"""
import os
import shutil

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model
from apps.catalog.models import topics_group, topic_section, post, postarchivo

User = get_user_model()
PASSWORD = "sharp2026"

BASE = os.path.dirname(os.path.abspath(__file__))
MEDIA = settings.MEDIA_ROOT


def portada(nombre):
    """Copia la foto de static a MEDIA y devuelve la ruta para guardarla.

    El campo 'imagen' de topics_group es un ImageField, y Django arma la
    direccion como /media/<lo que se guarde>. Las fotos estan en static/,
    donde no existe /media/, asi que la portada daba 404. Copiandolas a
    MEDIA quedan igual que una portada subida por un usuario.
    """
    origen = os.path.join(BASE, "apps", "catalog", "static", "catalog", "img", nombre)
    carpeta = os.path.join(MEDIA, "catalog", "group", "image")
    destino = os.path.join(carpeta, nombre)
    if not os.path.exists(destino):
        os.makedirs(carpeta, exist_ok=True)
        shutil.copyfile(origen, destino)
    return "catalog/group/image/" + nombre

# ---------------------------------------------------------------------------
# Los avatares
#
# El campo imagen de customuser trae de fabrica la misma imagen para todo el
# mundo (/users/imagenes/user.jpg), asi que los cuatro se veian iguales.
# Aqui se dibuja uno por persona: un circulo de color con sus iniciales.
# Para poner una foto real basta con cambiar el archivo del avatar desde el
# perfil; esto solo es el dato de arranque.
# ---------------------------------------------------------------------------
TAM = 225


def dibujar_avatar(iniciales, color):
    """Devuelve los bytes JPEG de un avatar: circulo de color + iniciales."""
    from io import BytesIO
    from PIL import Image, ImageDraw, ImageFont

    imagen = Image.new("RGB", (TAM, TAM), "#17112b")
    dibujo = ImageDraw.Draw(imagen)
    dibujo.ellipse((0, 0, TAM - 1, TAM - 1), fill=color)

    try:
        fuente = ImageFont.truetype("arialbd.ttf", int(TAM * 0.42))
    except OSError:
        fuente = ImageFont.load_default()

    # textbbox devuelve el borde del texto; se resta para que la caja de la
    # letra quede centrada y no un poco corrida a la izquierda.
    caja = dibujo.textbbox((0, 0), iniciales, font=fuente)
    x = (TAM - (caja[2] - caja[0])) / 2 - caja[0]
    y = (TAM - (caja[3] - caja[1])) / 2 - caja[1]
    dibujo.text((x, y), iniciales, font=fuente, fill="white")

    buffer = BytesIO()
    imagen.save(buffer, format="JPEG", quality=90)
    return buffer.getvalue()


# clave del usuario -> (iniciales, color de fondo)
AVATARES = {
    "camila": ("CR", "#7C3AED"),
    "jhonatan": ("JM", "#2563EB"),
    "laura": ("LO", "#DB2777"),
    "andres": ("AV", "#D97706"),
}

# Se borran todos los avatares viejos de estos cuatro usuarios antes de
# empezar. Si no, el nombre "camila.jpg" sigue ocupado por un archivo de una
# corrida anterior y Django guarda el nuevo como "camila_VKSTseF.jpg",
# dejando la carpeta llena de copias.
# Lo que no se toca es user.jpg, que es el avatar por defecto del modelo.
CARPETA_AVATARES = os.path.join(MEDIA, "users", "avatares")
if os.path.isdir(CARPETA_AVATARES):
    for archivo in os.listdir(CARPETA_AVATARES):
        for clave in AVATARES:
            if archivo.startswith(clave):
                os.remove(os.path.join(CARPETA_AVATARES, archivo))


# ---------------------------------------------------------------------------
# Las personas
# ---------------------------------------------------------------------------
PERSONAS = {
    "camila": dict(
        first_name="Camila", last_name="Restrepo", email="camila@gmail.com",
        bio="Tecnico en electromecanada. Aqui pregunto lo que no entiendo."),
    "jhonatan": dict(
        first_name="Jhonatan", last_name="Morales", email="jhonatan@gmail.com",
        bio="Tecnico en desarrollo. Si tiene mas de tres pasos, no lo explico."),
    "laura": dict(
        first_name="Laura", last_name="Ospina", email="laura@gmail.com",
        bio="Ciencias sociales. Pregunto mucho, aunque ya me lo hayan explicado."),
    "andres": dict(
        first_name="Andres", last_name="Villa", email="andres@gmail.com",
        bio="Salud. Respondo todo y me quejo de todo."),
}

usuarios = {}
for clave, datos in PERSONAS.items():
    u, creado = User.objects.get_or_create(
        username=clave,
        defaults={
            "first_name": datos["first_name"],
            "last_name": datos["last_name"],
            "email": datos["email"],
        },
    )
    u.first_name = datos["first_name"]
    u.last_name = datos["last_name"]
    u.email = datos["email"]
    u.set_password(PASSWORD)

    # Avatar propio. Si ya habia uno generado antes se borra el archivo
    # viejo, para no dejar copias repetidas en media al reejecutar. Se mira
    # solo el nombre del archivo: en la base la ruta es
    # "users/avatares/camila.jpg", que no empieza por "camila".
    from django.core.files.base import ContentFile
    if os.path.basename(u.imagen.name or "").startswith(clave):
        u.imagen.delete(save=False)
    iniciales, color = AVATARES[clave]
    u.imagen.save(clave + ".jpg", ContentFile(dibujar_avatar(iniciales, color)), save=False)

    u.save()
    usuarios[clave] = u
    print("  usuario {:<9} {}  avatar={}".format(
        clave, "creado" if creado else "ya existia", u.imagen.name))

CAMILA = usuarios["camila"]
JHON = usuarios["jhonatan"]
LAURA = usuarios["laura"]
ANDRES = usuarios["andres"]

# ---------------------------------------------------------------------------
# Los grupos
# ---------------------------------------------------------------------------
GRUPOS = [
    dict(
        nombre="Ingles conversacional",
        descripcion="Para practicar speaking sin pena. Resolvemos las frases que "
                    "nos trancan en la vida diaria: pedir la cuenta, pedir "
                    "perdón, entender cuando hablan rápido.",
        categoria="idiomas",
        imagen="reading1.jpg",
        dueno=CAMILA,
        secciones=["Vocabulario util", "Expresiones del dia a dia"],
    ),
    dict(
        nombre="Matematicas: calculo diferencial",
        descripcion="Limites, derivadas y sus aplicaciones. Si alguien se queda "
                    "atrapado en un ejercicio, se escribe y lo resolvemos entre "
                    "todos.",
        categoria="matematicas",
        imagen="fieren_python.jpg",
        dueno=JHON,
        secciones=["Limites", "Derivadas", "Aplicaciones"],
    ),
    dict(
        nombre="Ateismo: pensar sin respuesta facil",
        descripcion="Debates sobre existencia, sentido y moral. Aqui se discute "
                    "con respeto y se citan textos, no sientes.",
        categoria="filosofia",
        imagen="cuadernos.jpg",
        dueno=LAURA,
        secciones=["Debates", "Lecturas"],
    ),
]

grupos = {}
for datos in GRUPOS:
    # La portada se copia una sola vez por grupo, no una por cada vez que se
    # toca el grupo.
    foto_grupo = portada(datos["imagen"])

    g, creado = topics_group.objects.get_or_create(
        nombre=datos["nombre"],
        defaults={
            "descripcion": datos["descripcion"],
            "categoria": datos["categoria"],
            "imagen": foto_grupo,
            "creator": datos["dueno"],
        },
    )
    g.descripcion = datos["descripcion"]
    g.categoria = datos["categoria"]
    g.imagen = foto_grupo
    g.creator = datos["dueno"]
    g.save()
    grupos[datos["nombre"]] = g
    print("  grupo    {:<36} {}".format(datos["nombre"], "creado" if creado else "ya existia"))

    for nombre in datos["secciones"]:
        topic_section.objects.get_or_create(name=nombre, group=g)

    # Todos se suscriben a todos los grupos.
    for u in usuarios.values():
        g.subscriptions.add(u)

INGLES = grupos["Ingles conversacional"]
MATES = grupos["Matematicas: calculo diferencial"]
ATEISMO = grupos["Ateismo: pensar sin respuesta facil"]

# ---------------------------------------------------------------------------
# Las conversaciones
# Cada tupla es: (grupo, autor, texto, adjunto, respuestas)
# y una respuesta es (autor, texto, adjunto).
# ---------------------------------------------------------------------------

CONVERSACIONES = [
    # ------------------------------ INGLES ---------------------------------
    (INGLES, CAMILA,
     "Alguien sabe un metodo para aprender ingles mas rapido? Llevo dos anos y "
     "siento que no avanzo nada. Veo videos, hago ejercicios, pero a la semana "
     "se me ha olvidado todo.",
     None,
     [
         (JHON, "Lo que a mi me sirvio fue dejar de estudiar palabras sueltas y "
                "empezar con frases completas. \"Tengo hambre\" se te pega mucho "
                "mas que la palabra \"hambre\" sola. Y usarlas al dia siguiente, "
                "aunque sea hablando solo en la casa.", None),
         (ANDRES, "Busca una serie que ya te guste y ponle subtitulos en ingles, "
                  "no en espanol. Como ya conoces la historia, terminas "
                  "entendiendo el doble de lo que crees.", None),
         (LAURA, "Yo uso flashcards pero diez minutos al dia. Lo que me mata es "
                 "hacerlo dos horas el domingo y al lunes no haber retenido nada.",
          None),
         (JHON, "+1 a Laura. Diez minutos todos los dias le gana a dos horas el "
                 "domingo.", None),
         (CAMILA, "Dos anos explicando mi problema y era pura constancia, no "
                  "metodo. Carajo que rabia tener que aprender todo a la mala.",
          None),
     ]),

    (INGLES, ANDRES,
     "Siguiendo con el tema: como se dice \"me equivoque de mesa\" sin que "
     "suene a que estoy reclamando?",
     None,
     [
         (CAMILA, "\"Sorry, I think this table is taken.\" Con sorry al principio "
                   "suena a error mio, no a reclamo.", None),
         (LAURA, "A mi me paso igual, es super normal. \"Excuse me, could we have "
                 "the bill, please?\" y ya esta. Y no te disculpes tanto parce que "
                 "peor queda. Les dejo un gato de consuelo:",
          "catalog/static/catalog/img/gato2.jpg"),
     ]),

    (INGLES, LAURA,
     "Cual es la diferencia entre \"I have been\" y \"I had been\"? Mi profe lo "
     "explica y no entiendo cuando va cada uno.",
     None,
     [
         (JHON, "\"I had been\" es para algo que empezo antes de otro pasado. "
                 "\"Cuando llegue, yo habia comido.\" Si no hay otro pasado antes, "
                 "usa \"I have been\".", None),
         (ANDRES, "Eso, es como hablar de dos cosas a la vez. Y a cual de las dos "
                  "pregunto?", None),
     ]),

    (INGLES, CAMILA,
     "Ultima del dia y lo prometo: como pido la cuenta sin que el mesero se "
     "ofenda? Ayer me quedé callada como diez segundos esperando que se me "
     "ocurriera algo.",
     None,
     [
         (LAURA, "A mi me paso igual, es super normal. \"Excuse me, could we have "
                 "the bill, please?\" y ya esta. No te disculpes tanto parce que "
                 "peor queda.", None),
         (ANDRES, "En el pais es \"la cuenta\" normalito, ahi toca el "
                  "\"excuse me\" si te sientes rara.", None),
     ]),

    # ---------------------------- MATEMATICAS -----------------------------
    (MATES, LAURA,
     "Alguien me explica como se usa la regla de L'Hopital? Entiendo que es "
     "para los casos 0/0, pero no me queda claro cuando aplicarla y cuando el "
     "limite simplemente no existe.",
     None,
     [
         (JHON, "Derivas numerador y denominador por separado y vuelves a "
                "calcular el limite. Si te da un numero, ese es el limite. Si te "
                "sigue dando 0/0 o indefinido, la regla no aplicaba y toca otro "
                "metodo.", None),
         (CAMILA, "Y nunca sirve para 0/2 o 5/infinito? Esas no son 0/0.", None),
         (JHON, "Jamás. Solo funciona con 0/0 y con infinito sobre infinito. En "
                 "los demas casos el limite se calcula normal, dividiendo.", None),
         (ANDRES, "Un truco que me salvo el parcial: si despues de derivar te "
                  "sigue dando 0/0, casi siempre es que te equivocaste en la "
                  "derivada, no que el metodo falle. Repasala antes de cambiar de "
                  "cosa.", None),
         (LAURA, "Con lo de repasar la derivada me di cuenta de que tenia mal y "
                 "ya me salio. No puedo con esta materia, en serio.", None),
     ]),

    (MATES, LAURA,
     "Para un parcial conviene Simpson o trapezoidal? El enunciado no dice "
     "cual y no quiero aplicar el que no es.",
     "catalog/static/catalog/img/cuadernos.jpg",
     [
         (CAMILA, "Mira primero que pide el enunciado. Si no dice nada, Simpson da "
                   "mas precision con menos puntos, pero es mas largo de hacer a "
                   "mano.", None),
         (ANDRES, "Y trapezoidal es mas facil a mano. Si no dejan calculadora, ni "
                  "lo pienses.", None),
         (LAURA, "O sea que todo depende del enunciado. Este profesor no nos "
                 "ayuda para nada.", None),
     ]),

    (MATES, JHON,
     "Alguien sabe como saber si una serie converge sin usar el test de la razon? "
     "Ese test no me sirve para casi todas.",
     None,
     [
         (JHON, "Si converge, el de la razon a veces no aplica, pero el de la raiz "
                "o el de la comparacion si. Tambien el criterio integral, que "
                "cubre casi todo.", None),
         (ANDRES, "El de comparacion es el que mas salva en parciales: comparas "
                  "con una serie que ya te sabes de memoria.", None),
         (CAMILA, "Voy a anotar el integral porque ese no lo habia visto en ningun "
                   "video que vi.", None),
     ]),

    # ------------------------------ ATEISMO -------------------------------
    (ATEISMO, LAURA,
     "Pregunta para el debate: si Dios no existe, el sentido de la vida se "
     "construye o se descubre? Me dicen que \"se construye\" pero me suena a "
     "que es una forma de evadir la pregunta.",
     None,
     [
         (ANDRES, "Se construye, parzivis. Nadie nace con un proposito ya "
                  "terminado; lo vas armando con lo que haces. Si te vas akak en "
                  "el plan ya tienes el sentido que necesitas.", None),
         (JHON, "Ojo que \"tiene sentido\" y \"se construyó\" no es lo mismo. "
                 "Podés construir una vida con sentido sin que nadie la haya "
                 "planeado. Eso no es un problema, es una diferencia.", None),
         (CAMILA, "Yo diria que se descubre, pero de forma indirecta: te vas "
                   "descubriendo a vos mientras haces algo que te importa de "
                   "verdad. Igual lo de Jhonatan me gusta mas.", None),
         (LAURA, "Me sirvio un montón eso ultimo. Es que siempre me han repetido "
                  "\"el sentido se busca\" como si fuera adivinacion y ya.", None),
     ]),

    (ATEISMO, ANDRES,
     "Alguien tiene un texto corto para citar? Busco algo que no sean 400 "
     "paginas y que no sea un sermon.",
     None,
     [
         (LAURA, "El primer capitulo de El mito de Siso de Camus va justo de eso. "
                 "Es corto y no se pone solemne.", None),
         (JHON, "Y si queres algo mas reciente, El miedo a preguntar de Leopoldo "
                 "Roscoe.", None),
         (CAMILA, "Yo no he leido nada del tema, alguien tiene algo para empezar "
                   "de cero sin que me explote la cabeza?", None),
     ]),
]


def adjuntar(origen, post_obj):
    """Devuelve un postarchivo con el archivo dentro, todavia sin guardar.

    Se lee de una vez a memoria (ContentFile) y no con un archivo abierto:
    con "with open(...)" el archivo se cerraba antes de que Django lo
    escribiera y salia "ValueError: seek of closed file"."""
    from django.core.files.base import ContentFile
    with open(origen, "rb") as archivo:
        contenido = archivo.read()
    return postarchivo(
        post=post_obj,
        archivo=ContentFile(contenido, name=os.path.basename(origen)),
        nombre_original=os.path.basename(origen),
    )


# ---------------------------------------------------------------------------
# Limpieza: para que este script se pueda volver a ejecutar sin duplicar nada,
# se quitan primero las publicaciones del intento anterior. Las respuestas van
# en cascada, asi que tambien se van con ellas.
# ---------------------------------------------------------------------------
TEXTOS_DEMO = {texto for _, _, texto, _, _ in CONVERSACIONES}
borrados = post.objects.filter(content__in=TEXTOS_DEMO).delete()[0]
if borrados:
    print("  se quitaron {} publicaciones de un intento anterior".format(borrados))

# Los archivos de esos adjuntos quedan huerfanos en media, asi que se limpia
# la carpeta antes de volver a adjuntar.
CARPETA_ADJUNTOS = os.path.join(MEDIA, "catalog", "post", "archivos")
if os.path.isdir(CARPETA_ADJUNTOS):
    for carpeta, _, archivos in os.walk(CARPETA_ADJUNTOS, topdown=False):
        for archivo in archivos:
            os.remove(os.path.join(carpeta, archivo))

posts_creados = 0
respuestas_creadas = 0
adjuntos_creados = 0

for grupo, autor, texto, imagen, respuestas in CONVERSACIONES:
    p = post.objects.create(content=texto, user=autor, group=grupo)

    if imagen:
        ruta = os.path.join(BASE, "apps", imagen.replace("catalog/", "catalog/", 1))
        # La imagen se busca dentro del proyecto.
        candidatas = [
            os.path.join(BASE, "apps", imagen),
            os.path.join(BASE, "apps", "catalog", "static", "catalog", "img",
                         os.path.basename(imagen)),
            os.path.join(BASE, imagen),
        ]
        encontrada = next((c for c in candidatas if os.path.exists(c)), None)
        if encontrada:
            adjunto = adjuntar(encontrada, p)
            adjunto.save()
            adjuntos_creados += 1
            print("    adjunto: {}".format(adjunto.nombre_original))
        else:
            print("    NO SE ENCONTRO la imagen {}".format(imagen))

    posts_creados += 1

    for r_autor, r_texto, r_imagen in respuestas:
        respuesta = post.objects.create(content=r_texto, user=r_autor, parent=p)
        respuestas_creadas += 1
        if r_imagen:
            encontrada = None
            candidatas = [
                os.path.join(BASE, "apps", r_imagen),
                os.path.join(BASE, "apps", "catalog", "static", "catalog", "img",
                             os.path.basename(r_imagen)),
            ]
            encontrada = next((c for c in candidatas if os.path.exists(c)), None)
            if encontrada:
                adjunto = adjuntar(encontrada, respuesta)
                adjunto.save()
                adjuntos_creados += 1
                print("    adjunto en una respuesta: {}".format(adjunto.nombre_original))

# ---------------------------------------------------------------------------
# Secciones
#
# La maquinaria de secciones funciona (crear, renombrar, borrar, publicar y
# ver), pero sin esto las 7 secciones quedan vacias y al abrirlas sale
# "Esta seccion todavia no tiene publicaciones", que parece que esta roto.
# Se mete una publicacion en cada seccion, empezando por la mas antigua del
# grupo que todavia no este en ninguna.
#
# Ojo: el post sigue apareciendo tambien en la pagina del grupo, porque la
# pagina del grupo lista todas las publicaciones del grupo sin importar la
# seccion. Es duplicado a proposito (la seccion es una vista), pero si se
# quiere que cada post este en una sola seccion, hay que filtrar el grupo.
# ---------------------------------------------------------------------------
en_secciones = 0
for grupo in grupos.values():
    for seccion in grupo.sections.all():
        # Ojo: no se puede filtrar con
        #   .exclude(id__in=topic_section.objects.values_list("posts__id", flat=True))
        # porque las secciones vacias aportan un None, y "id IN (NULL)" es
        # NULL en SQL: eso excluye TODAS las filas y no mete nada.
        # Por la relacion inversa se hace: post que no esta en ninguna seccion.
        candidatos = grupo.post.filter(parent__isnull=True).exclude(
            topic_section__isnull=False)
        primero = candidatos.first()
        if primero:
            seccion.posts.add(primero)
            en_secciones += 1

print("  publicaciones metidas en secciones: {}".format(en_secciones))

# ---------------------------------------------------------------------------
# Likes y score
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Likes y score
#
# Ojo: los POSTS no tienen campo likes (solo existe en la tabla vieja, pero
# no en el modelo). Los likes van en los GRUPOS: es lo unico que puntua.
# ---------------------------------------------------------------------------
LIKES_DE_GRUPOS = {
    "Ingles conversacional": [CAMILA, ANDRES, JHON],
    "Matematicas: calculo diferencial": [LAURA, JHON, ANDRES, CAMILA],
    "Ateismo: pensar sin respuesta facil": [LAURA, JHON, CAMILA],
}

for nombre_grupo, quien in LIKES_DE_GRUPOS.items():
    g = grupos[nombre_grupo]
    for u in quien:
        g.likes.add(u)

for g in grupos.values():
    g.recalcular_score()
    print("  grupo {:<36} score={}".format(g.nombre, g.score))

print()
print("  posts: {}  respuestas: {}  adjuntos: {}".format(
    posts_creados, respuestas_creadas, adjuntos_creados))
print("  TOTAL en la base: {} usuarios, {} grupos, {} secciones, {} posts".format(
    User.objects.count(), topics_group.objects.count(),
    topic_section.objects.count(), post.objects.count()))
print("  clave de los 4 usuarios: {}".format(PASSWORD))