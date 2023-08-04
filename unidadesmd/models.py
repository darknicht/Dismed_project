from django.db import models

class UnidadMedica(models.Model):
    idudm = models.AutoField(primary_key=True)
    uni_codigo = models.IntegerField(max_length=32)
    cod_um_as400 = models.IntegerField(max_length=32)
    cod_esigef = models.IntegerField(max_length=32)
    cod_crp = models.CharField(max_length=255)
    nombre_unidad = models.CharField(max_length=255)
    nom_corto_unidad = models.CharField(max_length=255)
    nivel_atencion = models.CharField(max_length=255)
    tipologia_homo = models.CharField(max_length=255)
    complejidad = models.IntegerField(max_length=32)
    categ_establecimiento = models.CharField(max_length=255)
    coord_provincial = models.CharField(max_length=255)
    provincia = models.CharField(max_length=255)
    cod_prov = models.IntegerField(max_length=32)
    canton = models.CharField(max_length=255)
    cod_cant = models.IntegerField(max_length=32)
    parroquia = models.CharField(max_length=255)
    cod_parroquia = models.IntegerField(max_length=32)
    zona = models.CharField(max_length=255)
    distrito = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'unidadesmd'