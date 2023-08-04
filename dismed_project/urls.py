from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('inicio.urls')),
    path('buscador/', include('buscador.urls')),
    path('departamentos/', include('departamentos.urls')),
    path('admin/', admin.site.urls),


]
