from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MatrizDispositivos

@receiver(post_save, sender=MatrizDispositivos)
def actualizar_proyecc_saldo(sender, instance, **kwargs):
    if instance.perioci_consumo == "Mensual":
        proyecc_saldo = max(instance.saldo_bodega_actual - instance.consumo_prom_proyec * 3, 0)
    elif instance.perioci_consumo == "Semestral":
        proyecc_saldo = max(instance.saldo_bodega_actual - instance.consumo_prom_proyec * 0.5, 0)
    else:
        proyecc_saldo = max(instance.saldo_bodega_actual - instance.consumo_prom_proyec * 0.25, 0)
    
    instance.proyecc_saldo = proyecc_saldo
    instance.save()