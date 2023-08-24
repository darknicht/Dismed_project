from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Preseleccion, PrePriorizacion, Priorizacion
from listado_dispositivos_medicos.models import ListadoDispositivosMedicos
from listado_dispositivos_medicos.utils import get_nivel_atencion_queries


@login_required
def preseleccion_view(request):
    if request.method == "POST":
        seleccionados_ids = request.POST.getlist("seleccionados")
        if len(seleccionados_ids) < 5:
            messages.error(request, 'Por favor, selecciona al menos 5 items.')
            return redirect("preseleccion_view")

        dispositivos_seleccionados = ListadoDispositivosMedicos.objects.filter(
            id__in=seleccionados_ids
        )

        preseleccion = Preseleccion(usuario=request.user)
        preseleccion.save()
        preseleccion.dispositivos.add(*dispositivos_seleccionados)

        return redirect("prepriorizacion_view", preseleccion_id=preseleccion.id)

    else:
        nivel_atencion_queries = get_nivel_atencion_queries(request.user)
        dispositivos_list = ListadoDispositivosMedicos.objects.filter(
            nivel_atencion_queries
        ).order_by('id')

        paginator = Paginator(dispositivos_list, 20)  # 25 dispositivos por página
        page_number = request.GET.get("page")
        dispositivos = paginator.get_page(page_number)

        return render(request, "preseleccion.html", {"dispositivos": dispositivos})

@login_required
def prepriorizacion_view(request, preseleccion_id):
    preseleccion = Preseleccion.objects.get(pk=preseleccion_id)
    # Resto de la lógica para manejar la pre-priorización

    return render(request, "prepriorizacion.html", {"preseleccion": preseleccion})


@login_required
def priorizacion_view(request, pre_priorizacion_id):
    pre_priorizacion = PrePriorizacion.objects.get(pk=pre_priorizacion_id)
    # Resto de la lógica para manejar la priorización

    return render(request, "priorizacion.html", {"pre_priorizacion": pre_priorizacion})


# Puedes continuar agregando las vistas necesarias para tu flujo de trabajo
