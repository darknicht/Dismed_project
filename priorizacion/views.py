from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Preseleccion, PrePriorizacion, Priorizacion
from listado_dispositivos_medicos.models import ListadoDispositivosMedicos
from listado_dispositivos_medicos.utils import get_nivel_atencion_queries
from matriz_dispositivos.signals import actualizar_valores
from matriz_dispositivos.models import Periodo
from decimal import Decimal
import re


def parse_usd(value, decimals=2):
    pattern = r"^USD\s?\d{1,3}(,\d{3})*(\.\d{2})?$"
    if re.match(pattern, value) is not None:
        # Remove the currency symbol and replace the comma with nothing
        value = value.replace("USD", "").replace(",", "")
        return Decimal(value).quantize(Decimal(f"0.{decimals * '0'}"))
    else:
        raise ValueError("Formato USD inválido")


@login_required
def preseleccion_view(request):
    if request.method == "POST":
        seleccionados_ids = request.POST.getlist("seleccionados")
        if len(seleccionados_ids) < 5:
            messages.error(request, "Por favor, selecciona al menos 5 items.")
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
        ).order_by("id")

        paginator = Paginator(dispositivos_list, 20)  # 25 dispositivos por página
        page_number = request.GET.get("page")
        dispositivos = paginator.get_page(page_number)

        return render(request, "preseleccion.html", {"dispositivos": dispositivos})


@login_required
def prepriorizacion_view(request, preseleccion_id):
    preseleccion = Preseleccion.objects.get(pk=preseleccion_id)
    dispositivos_preseleccionados = preseleccion.dispositivos.all()

    # Obtener las opciones de periodicidad
    periodos = Periodo.objects.all()

    if request.method == "POST":
        for dispositivo in dispositivos_preseleccionados:
            try:
                perioci_consumo = request.POST.get(f"perioci_consumo_{dispositivo.id}")
                consumo_prom_proyec = request.POST.get(f"consumo_prom_proyec_{dispositivo.id}")
                cant_pend_entre = request.POST.get(f"cant_pend_entre_{dispositivo.id}")
                saldo_bodega_actual = request.POST.get(f"saldo_bodega_actual_{dispositivo.id}")
                prec_unit_ref = parse_usd(
                    request.POST.get(f"prec_unit_ref_{dispositivo.id}"), decimals=4
                )
                pres_ref_total = parse_usd(
                    request.POST.get(f"pres_ref_total_{dispositivo.id}")
                )
                prim_cuatri_mont = parse_usd(
                    request.POST.get(f"prim_cuatri_mont_{dispositivo.id}")
                )
                seg_cuatri_mont = parse_usd(
                    request.POST.get(f"seg_cuatri_mont_{dispositivo.id}")
                )
                terc_cuatri_mont = parse_usd(
                    request.POST.get(f"terc_cuatri_mont_{dispositivo.id}")
                )
            except ValueError:
                messages.error(
                    request,
                    f"Formato USD inválido para el dispositivo {dispositivo.id}. Asegúrate de usar el número correcto de decimales y el símbolo USD.",
                )
                return redirect("prepriorizacion_view", preseleccion_id=preseleccion_id)

            cod_proceso = request.POST.get(f"cod_proceso_{dispositivo.id}")
            tip_proc_cp = request.POST.get(f"tip_proc_cp_{dispositivo.id}")
            priorizacion = request.POST.get(f"priorizacion_{dispositivo.id}")
            observaciones = request.POST.get(f"observaciones_{dispositivo.id}")

            # Crear o actualizar el registro de PrePriorizacion
            pre_priorizacion, created = PrePriorizacion.objects.get_or_create(
                preseleccion=preseleccion,
                dispositivo=dispositivo,
            )
            pre_priorizacion.perioci_consumo = perioci_consumo
            pre_priorizacion.consumo_prom_proyec = consumo_prom_proyec
            pre_priorizacion.cant_pend_entre = cant_pend_entre
            pre_priorizacion.cod_proceso = cod_proceso
            pre_priorizacion.saldo_bodega_actual = saldo_bodega_actual
            pre_priorizacion.prec_unit_ref = prec_unit_ref
            pre_priorizacion.tip_proc_cp = tip_proc_cp
            pre_priorizacion.priorizacion = priorizacion
            pre_priorizacion.observaciones = observaciones

            # Llamar a la función que realiza los cálculos
            actualizar_valores(sender=PrePriorizacion, instance=pre_priorizacion)

            pre_priorizacion.save()

        # Redireccionar a la siguiente etapa (por ejemplo, Priorización)
        return redirect("priorizacion_view", preseleccion_id=preseleccion.id)

    return render(
        request,
        "prepriorizacion.html",
        {
            "dispositivos": dispositivos_preseleccionados,
            "periodos": periodos,
        },
    )


@login_required
def priorizacion_view(request, pre_priorizacion_id):
    pre_priorizacion = PrePriorizacion.objects.get(pk=pre_priorizacion_id)
    # Resto de la lógica para manejar la priorización

    return render(request, "priorizacion.html", {"pre_priorizacion": pre_priorizacion})


# Puedes continuar agregando las vistas necesarias para tu flujo de trabajo
