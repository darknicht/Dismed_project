# backup_manager/urls.py

from django.urls import path
from .views import crear_backup

urlpatterns = [
    path('crear/', crear_backup, name='crear_backup'),
]
