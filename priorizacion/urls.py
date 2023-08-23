from django.urls import path
from priorizacion import views as priorizacion_views

urlpatterns = [
    path(
        "preseleccion/", priorizacion_views.preseleccion_view, name="preseleccion_view"
    ),
    path(
        "prepriorizacion/<int:preseleccion_id>/",
        priorizacion_views.prepriorizacion_view,
        name="prepriorizacion_view",
    ),
    path(
        "priorizacion/", priorizacion_views.priorizacion_view, name="priorizacion_view"
    ),
]
