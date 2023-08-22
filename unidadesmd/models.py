from django.db import models

class UnidadMedica(models.Model):
    idudm = models.AutoField(primary_key=True)
    uni_codigo = models.IntegerField()
    cod_um_as400 = models.IntegerField()
    cod_esigef = models.IntegerField()
    cod_crp = models.CharField(max_length=255)
    nombre_unidad = models.CharField(max_length=255)
    nom_corto_unidad = models.CharField(max_length=255)
    nivel_atencion = models.CharField(max_length=255)
    tipologia_homo = models.CharField(max_length=255)
    complejidad = models.IntegerField()
    categ_establecimiento = models.CharField(max_length=255)
    coord_provincial = models.CharField(max_length=255)
    provincia = models.CharField(max_length=255)
    cod_prov = models.IntegerField()
    canton = models.CharField(max_length=255)
    cod_cant = models.IntegerField()
    parroquia = models.CharField(max_length=255)
    cod_parroquia = models.IntegerField()
    zona = models.CharField(max_length=255)
    distrito = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nombre_unidad
    
    class Meta:
        db_table = 'unidadesmd'