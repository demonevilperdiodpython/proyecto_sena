from django.db import migrations, models
import django.db.models.deletion
import apps.catalog.models


class Migration(migrations.Migration):
    """Un solo modelo para los adjuntos del post.

    Se escribe a mano a proposito: makemigrations genera tambien un
    RemoveField de post.likes y post.dislikes (campos que estan en la base
    de datos pero no en el modelo), y al aplicarla se rompian los likes.

    Los modelos postimagen y postvideo no se tocan: los posts que ya tienen
    una imagen o un video siguen mostrandolos."""

    dependencies = [
        ('catalog', '0006_upload_rutas'),
    ]

    operations = [
        migrations.CreateModel(
            name='postarchivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to=apps.catalog.models.ruta_con_fecha('catalog/post/archivos'))),
                ('nombre_original', models.CharField(blank=True, max_length=255)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='archivos', to='catalog.post')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]