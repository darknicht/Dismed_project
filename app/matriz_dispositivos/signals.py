from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import MatrizDispositivos, Periodo

#Calcula Proyección de Saldo (PS)
def calcular_proyecc_saldo(instance):
    if instance.perioci_consumo == "Mensual":
        return max(instance.saldo_bodega_actual - instance.consumo_prom_proyec * 3, 0)
    elif instance.perioci_consumo == "Semestral":
        return max(instance.saldo_bodega_actual - instance.consumo_prom_proyec * 0.5, 0)
    else:
        return max(instance.saldo_bodega_actual - instance.consumo_prom_proyec * 0.25, 0)

#Calcula Requerimiento Total Proyectado (RTP)
def calcular_req_total_proyectado(instance):
    matriz_value_actual = Periodo.objects.get(periodicidad=instance.perioci_consumo).matriz_value
    temp_value = instance.consumo_prom_proyec * matriz_value_actual - (instance.proyecc_saldo + instance.cant_pend_entre)
    return 0 if temp_value < 0 else temp_value

#Calcula Stock de Seguridad (SS)
def calcular_stock_seguridad(instance):
    periodo = Periodo.objects.get(periodicidad=instance.perioci_consumo)
    if instance.perioci_consumo == "Mensual":
        temp_value = instance.consumo_prom_proyec * periodo.matriz_value + instance.consumo_prom_proyec * periodo.stock_seguridad - (instance.proyecc_saldo + instance.cant_pend_entre)
        if temp_value <= 0:
            return 0
        elif instance.req_total_proyectado > 0:
            return instance.consumo_prom_proyec * periodo.stock_seguridad
        elif instance.req_total_proyectado <= 0 and temp_value > 0:
            return temp_value
    return 0  # Retorno predeterminado para otros periodos

#Calcula Cantidad a Programar Inicial (CPI)
def calcular_cant_program_inicial(instance):
    temp_value = instance.req_total_proyectado + instance.stock_seguridad
    return temp_value if temp_value > 0 else 0

#Calcula Cantidad Final Requerida (CFR)
def calcular_cant_final_required(instance):
    if instance.cant_program_inicial > 0:
        return instance.cant_program_inicial + instance.cant_devol_prestam

    periodicidad_obj = Periodo.objects.get(periodicidad=instance.perioci_consumo)
    factor_1 = periodicidad_obj.factor
    factor_2 = periodicidad_obj.matriz_value

    temp_value = (instance.consumo_prom_proyec * factor_1 + instance.consumo_prom_proyec * factor_2 + instance.cant_devol_prestam) - (instance.proyecc_saldo + instance.cant_pend_entre)

    return 0 if temp_value < 0 else temp_value

#Calcula Precio de Referencia Total (PRT)
def calcular_pres_ref_total(instance):
    return instance.cant_final_required * instance.prec_unit_ref

#Calcula Disponibilidad del Dispositivo Médico (DDM)
def calcular_dispo_dm(instance):
    if instance.consumo_prom_proyec == 0:
        return 0

    if instance.perioci_consumo == "Mensual":
        return int((instance.proyecc_saldo + instance.cant_pend_entre) / instance.consumo_prom_proyec)
    elif instance.perioci_consumo == "Semestral":
        return int((instance.proyecc_saldo + instance.cant_pend_entre) / instance.consumo_prom_proyec * 6)
    else:
        return int((instance.proyecc_saldo + instance.cant_pend_entre) / instance.consumo_prom_proyec * 12)

#Calcula Nivel de Abastecimiento (NA)
def calcular_lvl_abastec(instance):
    if instance.consumo_prom_proyec > 0:
        if instance.dispo_dm == 0:
            return "STOCK 0"
        elif instance.dispo_dm > 0 and instance.dispo_dm <= 2:
            return "STOCK CRÍTICO"
        elif instance.dispo_dm > 2 and instance.dispo_dm <= 15:
            return "ABASTECIDO"
        else:
            return "SOBRESTOCK"
    else:
        return ""

#Calcula Cantidad Primera Cuatrimestre (PCC)
def calcular_prim_cuatri_cant(instance):
    condicion = instance.dispo_dm <= 4 and instance.seg_cuatri_cant <= 0
    if condicion:
        return instance.cant_final_required
    else:
        return 0

#Calcula Monto Primera Cuatrimestre (PCM)
def calcular_prim_cuatri_mont(instance):
    if instance.dispo_dm <= 4 and instance.seg_cuatri_mont <= 0:
        return instance.pres_ref_total
    else:
        return 0

#Calcula Cantidad Segunda Cuatrimestre (SCC)
def calcular_seg_cuatri_cant(instance):
    cond1 = 4 < instance.dispo_dm <= 8
    cond2 = instance.cant_program_inicial == 0 and instance.cant_devol_prestam > 0 and instance.cant_final_required > 0
    
    if cond1 or cond2:
        return instance.cant_final_required
    else:
        return 0

#Calcula Monto Segundo Cuatrimestre (SCM)
def calcular_seg_cuatri_mont(instance):
    # La primera parte (O) verifica si alguna de las condiciones dentro del paréntesis se cumple.
    # En este caso, la primera condición es Y(AG14>4;AG14<=8) y la segunda condición es Y(AB14=0;AC14>0;AD14>0)
    condicion_1 = 4 < instance.dispo_dm <= 8
    condicion_2 = instance.cant_program_inicial == 0 and instance.cant_devol_prestam > 0 and instance.cant_final_required > 0
    
    # Si alguna de las dos condiciones anteriores se cumple, se devuelve AF14, de lo contrario, se devuelve 0.
    if condicion_1 or condicion_2:
        return instance.pres_ref_total
    else:
        return 0

#Calcula Cantidad Tercer Cuatrimestre (TCC)
def calcular_terc_cuatri_cant(instance):
    # La condición verifica si las tres declaraciones dentro del paréntesis se cumplen simultáneamente.
    condicion = 8 < instance.dispo_dm <= 15 and instance.seg_cuatri_cant <= 0 and instance.cant_final_required > 0
    
    # Si la condición anterior se cumple, se devuelve AD14, de lo contrario, se devuelve 0.
    if condicion:
        return instance.cant_final_required
    else:
        return 0

#Calcula Monto Tercer Cuatrimestre (TCM)
def calcular_terc_cuatri_mont(instance):
    condicion = (instance.dispo_dm > 8) and (instance.dispo_dm <= 15) and (instance.seg_cuatri_mont <= 0)
    if condicion:
        return instance.pres_ref_total
    else:
        return 0

#Señal que se ejecuta antes de guardar un registro de MatrizDispositivos
@receiver(pre_save, sender=MatrizDispositivos)
def actualizar_valores(sender, instance, **kwargs):
    instance.proyecc_saldo = calcular_proyecc_saldo(instance)
    instance.req_total_proyectado = calcular_req_total_proyectado(instance)
    instance.stock_seguridad = calcular_stock_seguridad(instance)
    instance.cant_program_inicial = calcular_cant_program_inicial(instance)
    instance.cant_final_required = calcular_cant_final_required(instance)
    instance.pres_ref_total = calcular_pres_ref_total(instance)
    instance.dispo_dm = calcular_dispo_dm(instance)
    instance.lvl_abastec = calcular_lvl_abastec(instance)
    instance.prim_cuatri_cant = calcular_prim_cuatri_cant(instance)
    instance.prim_cuatri_mont = calcular_prim_cuatri_mont(instance)
    instance.seg_cuatri_cant = calcular_seg_cuatri_cant(instance)
    instance.seg_cuatri_mont = calcular_seg_cuatri_mont(instance)
    instance.terc_cuatri_cant = calcular_terc_cuatri_cant(instance)
    instance.terc_cuatri_mont = calcular_terc_cuatri_mont(instance)