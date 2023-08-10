from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('inicio.urls')),
    path('buscador/', include('buscador.urls')),
    path('departamentos/', include('departamentos.urls')),
    path('unidadesmd/', include('unidadesmd.urls')),
    path('matriz_dispositivos/', include('matriz_dispositivos.urls')),
    path('matriz_medicamentos/', include('matriz_medicamentos.urls')),
    path('importacion/', include('importacion.urls')),
    path('admin/', admin.site.urls),
]

# Si el proyecto está en modo DEBUG (desarrollo), entonces sirve los archivos media.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
