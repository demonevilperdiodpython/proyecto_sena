import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from django.conf import settings
settings.ALLOWED_HOSTS.append("testserver")

from django.test import Client
from django.urls import reverse
from apps.users.models import customuser

c = Client()

# Crear/obtener usuario de prueba
try:
    u = customuser.objects.filter(is_superuser=False).first()
    if not u:
        u = customuser.objects.create_user(username="testuser", email="test@gmail.com", password="test1234")
except Exception as e:
    print("user setup:", e)
    u = None

def get(path, follow=True):
    r = c.get(path, follow=follow)
    print(f"GET {path} -> {r.status_code}")
    if r.status_code >= 400:
        if hasattr(r, "exception") and r.exception:
            print("   exc:", repr(r.exception))
        else:
            print("   body snippet:", r.content[:300])

get("/")                      # home anon
if u:
    c.force_login(u)
    get("/")                  # home auth
    get("/settings/")
    get("/ia/")
    get("/popular/")
    get("/search/")
    get("/add_group/")
    # grupo y seccion existentes
    from apps.catalog.models import topics_group, topic_section
    g = topics_group.objects.first()
    if g:
        get(f"/group/{g.id}/")
        s = topic_section.objects.filter(group=g).first()
        if s:
            get(f"/group/{g.id}/section/{s.id}/")
            get(f"/group/{g.id}/section/{s.id}/post/")
        else:
            print("(no hay secciones para probar)")
    p = None
    from apps.catalog.models import post as post_model
    p = post_model.objects.first()
    if p:
        get(f"/post/{p.id}/")

    # Probar secciones con datos temporales
    from apps.catalog.models import topic_section as topic_section_model
    tmp = None
    try:
        tmp = topic_section_model.objects.create(name="SeccionPruebaTemp", group=g)
        get(f"/group/{g.id}/section/{tmp.id}/")
        get(f"/group/{g.id}/section/{tmp.id}/post/")
    finally:
        if tmp:
            tmp.delete()
    c.logout()
print("DONE")
