from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_customuser_admin_fk_customuser_created_groups_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='is_super_user',
            new_name='is_platform_admin',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_platform_admin',
            field=models.BooleanField(
                default=False,
                help_text='Moderador global de la aplicacion (no es el superusuario de Django).',
            ),
        ),
    ]
