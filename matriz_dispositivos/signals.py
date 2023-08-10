from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import MatrizDispositivos, Periodo 

@receiver(pre_save, sender=MatrizDispositivos)
def actualizar_proyecc_saldo(sender, instance, **kwargs):
    if instance.perioci_consumo == "Mensual":
        proyecc_saldo = max(instance.saldo_bodega_actual - instance.consumo_prom_proyec * 3, 0)
    elif instance.perioci_consumo == "Semestral":
        proyecc_saldo = max(instance.saldo_bodega_actual - instance.consumo_prom_proyec * 0.5, 0)
    else:
        proyecc_saldo = max(instance.saldo_bodega_actual - instance.consumo_prom_proyec * 0.25, 0)
    
    instance.proyecc_saldo = proyecc_saldo
    
    # Calcula req_total_proyectado
    matriz_value_actual = Periodo.objects.get(periodicidad=instance.perioci_consumo).matriz_value
    temp_value = instance.consumo_prom_proyec * matriz_value_actual - (instance.proyecc_saldo + instance.cant_pend_entre)

    # Implementación de la función SI
    if temp_value < 0:
        req_total_proyectado = 0
    else:
        req_total_proyectado = temp_value
        
    instance.req_total_proyectado = req_total_proyectado
