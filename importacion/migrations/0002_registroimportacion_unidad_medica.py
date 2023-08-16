# Generated by Django 4.2.3 on 2023-08-10 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unidadesmd', '0001_initial'),
        ('importacion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registroimportacion',
            name='unidad_medica',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='unidadesmd.unidadmedica'),
        ),
    ]