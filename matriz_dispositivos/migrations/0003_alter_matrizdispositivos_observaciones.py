# Generated by Django 4.2.3 on 2023-08-31 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matriz_dispositivos', '0002_alter_matrizdispositivos_observaciones'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matrizdispositivos',
            name='observaciones',
            field=models.CharField(max_length=255),
        ),
    ]
