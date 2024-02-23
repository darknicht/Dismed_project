# Generated by Django 4.2.3 on 2023-08-26 16:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listado_dispositivos_medicos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('priorizacion', '0003_remove_prepriorizacion_fecha_modificacion_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PrePriorizacion',
            new_name='Estimacion',
        ),
        migrations.RenameField(
            model_name='priorizacion',
            old_name='pre_priorizacion',
            new_name='pre_estimacion',
        ),
    ]