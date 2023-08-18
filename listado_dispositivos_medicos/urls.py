from django.urls import path
from .views import listado_dispositivos_medicos_view

urlpatterns = [
    path('', listado_dispositivos_medicos_view, name='listado_dispositivos_medicos'),
]
