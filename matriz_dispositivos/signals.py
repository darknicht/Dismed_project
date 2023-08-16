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

#Señal que se ejecuta antes de guardar un registro de MatrizDispositivos
@receiver(pre_save, sender=MatrizDispositivos)
def actualizar_valores(sender, instance, **kwargs):
    instance.proyecc_saldo = calcular_proyecc_saldo(instance)
    instance.req_total_proyectado = calcular_req_total_proyectado(instance)
    instance.stock_seguridad = calcular_stock_seguridad(instance)
    instance.cant_program_inicial = calcular_cant_program_inicial(instance)
