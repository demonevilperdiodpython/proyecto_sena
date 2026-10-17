import apps.users.models
from django.db import migrations, models


class Migration(migrations.Migration):
    """Solo cambia DONDE se guardan los avatares nuevos."""

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='imagen',
            field=models.ImageField(default='/users/imagenes/user.jpg', upload_to='users/avatares'),
        ),
    ]