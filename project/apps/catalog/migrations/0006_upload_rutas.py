import apps.catalog.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Solo cambia DONDE se guardan los archivos nuevos.

    No toca la base de datos: las rutas viejas siguen intactas y siguen
    funcionando. A partir de ahora cada archivo se guarda con nombre
    aleatorio y en subcarpetas por fecha, para que no se acumulen
    duplicados como '_aB3xY9z'.
    """

    dependencies = [
        ('catalog', '0005_topics_group_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topics_group',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to=apps.catalog.models.ruta_con_fecha('catalog/grupos')),
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to=apps.catalog.models.ruta_con_fecha('catalog/productos')),
        ),
        migrations.AlterField(
            model_name='postimagen',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to=apps.catalog.models.ruta_con_fecha('catalog/post/imagenes')),
        ),
        migrations.AlterField(
            model_name='postvideo',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to=apps.catalog.models.ruta_con_fecha('catalog/post/videos'), validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov'])]),
        ),
    ]