from django.db import migrations, models


class Migration(migrations.Migration):
    """Le quita la barra inicial al default del avatar.

    El default era "/users/imagenes/user.jpg". Con la barra inicial Django
    lee ese valor como una ruta absoluta del sistema (C:\\users\\imagenes),
    que queda fuera de MEDIA_ROOT, y ahi revienta con
    SuspiciousFileOperation en .path, .exists(), .open() y .size.

    Sin barra el valor es una ruta normal dentro de MEDIA, asi que todo eso
    funciona. La URL /media que genera es exactamente la misma con barra o
    sin ella (/media/users/imagenes/user.jpg), asi que no se ve ningun
    cambio en pantalla.

    Ojo: esto solo cambia el default, o sea lo que reciben los usuarios
    NUEVOS. Los que ya estaban guardados conservan la barra en la base y
    habria que corregirlos a mano. En la base actual no hace falta: ningun
    usuario la tiene.
    """

    dependencies = [
        ('users', '0002_upload_ruta_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='imagen',
            field=models.ImageField(default='users/imagenes/user.jpg', upload_to='users/avatares'),
        ),
        migrations.AlterField(
            model_name='imagen',
            name='imagen',
            field=models.ImageField(default='users/imagenes/user.jpg', upload_to='users/imagenes'),
        ),
    ]