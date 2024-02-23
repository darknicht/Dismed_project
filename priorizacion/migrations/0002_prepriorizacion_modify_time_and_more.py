# Generated by Django 4.2.3 on 2023-08-23 22:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('priorizacion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prepriorizacion',
            name='modify_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='prepriorizacion',
            name='user_create',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prepriorizacion_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='prepriorizacion',
            name='user_modify',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prepriorizacion_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='preseleccion',
            name='modify_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='preseleccion',
            name='user_create',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='preseleccion_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='preseleccion',
            name='user_modify',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='preseleccion_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='priorizacion',
            name='modify_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='priorizacion',
            name='user_create',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='priorizacion_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='priorizacion',
            name='user_modify',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='priorizacion_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='prepriorizacion',
            name='fecha_modificacion',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='preseleccion',
            name='fecha_creacion',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='priorizacion',
            name='fecha_priorizacion',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]