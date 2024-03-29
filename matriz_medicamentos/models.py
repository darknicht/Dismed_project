from django.db import models
from unidadesmd.models import UnidadMedica


class MatrizMedicamentos(models.Model):
    id = models.AutoField(primary_key=True)
    unidad_medica = models.ForeignKey(UnidadMedica, on_delete=models.CASCADE)
    version = models.IntegerField()
    matrix = models.IntegerField()
    item_nro = models.IntegerField()
    nom_subcomite = models.CharField(max_length=255)
    nro_partida_pres = models.IntegerField()
    nom_partida_pres = models.CharField(max_length=255)
    cudim = models.CharField(max_length=255)
    cod_iess = models.CharField(max_length=255)
    cod_as400 = models.IntegerField()
    nom_generico = models.CharField(max_length=255)
    espec_tec = models.CharField(max_length=255)
    pres_unimed = models.CharField(max_length=255)
    lvl_riesgo_suger = models.CharField(max_length=255)
    lvl_aten_ia = models.CharField(max_length=255)
    lvl_aten_ib = models.CharField(max_length=255)
    lvl_aten_ic = models.CharField(max_length=255)
    lvl_aten_ii = models.CharField(max_length=255)
    lvl_aten_iii = models.CharField(max_length=255)
    lvl_aten_aph = models.CharField(max_length=255)
    espec_subespec = models.CharField(max_length=255)
    consumo_prom_proyec = models.IntegerField()
    perioci_consumo = models.CharField(max_length=255)
    saldo_bodega_actual = models.IntegerField()
    proyecc_saldo = models.IntegerField()
    cant_pend_entre = models.IntegerField()
    cod_proceso = models.CharField(max_length=255)
    req_total_proyectado = models.IntegerField()
    stock_seguridad = models.IntegerField()
    cant_program_inicial = models.IntegerField()
    cant_devol_prestam = models.IntegerField()
    cant_final_required = models.IntegerField()
    prec_unit_ref = models.DecimalField(max_digits=10, decimal_places=4)
    pres_ref_total = models.DecimalField(max_digits=10, decimal_places=4)
    dispo_dm = models.IntegerField()
    lvl_abastec = models.CharField(max_length=255)
    tip_proc_cp = models.CharField(max_length=255)
    prim_cuatri_cant = models.IntegerField()
    prim_cuatri_mont = models.DecimalField(max_digits=10, decimal_places=4)
    seg_cuatri_cant = models.IntegerField()
    seg_cuatri_mont = models.DecimalField(max_digits=10, decimal_places=4)
    terc_cuatri_cant = models.IntegerField()
    terc_cuatri_mont = models.DecimalField(max_digits=10, decimal_places=4)
    priorizacion = models.BooleanField(default=False)
    observaciones = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    user_modify = models.CharField(max_length=255)
    modify_time = models.DateTimeField(auto_now=True)
    user_create = models.CharField(max_length=255)

    class Meta:
        db_table = "matriz_medicamentos"
