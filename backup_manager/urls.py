# backup_manager/urls.py

from django.urls import path
from .views import crear_backup, import_backup

urlpatterns = [
    path('crear/', crear_backup, name='crear_backup'),
    path('importar/', import_backup, name='import_backup'),
]
