from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """Esta migracion no hace nada: queda solo como punto de la cadena.

    El campo topics_group.creator ya lo anade la migracion 0003
    (0003_post_dislikes_post_likes_topics_group_creator). Al repetirlo aqui,
    una base de datos nueva fallaba con "duplicate column name: creator_id"
    y no dejaba empezar. En la base vieja no se notaba porque 0005 ya
    estaba marcada como aplicada.

    No se borra el archivo porque 0006 depende de ella."""

    dependencies = [
        ('catalog', '0004_topics_group_descripcion'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # El campo 'creator' ya lo agrega la migracion 0003 (ver el
        # docstring de la clase). Aqui no se repite.
    ]