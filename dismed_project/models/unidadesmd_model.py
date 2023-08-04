"""
Author: Christian Aguirre (christian.david.aguirre@gmail.com)
unidadesmd_model.py (c) 2023
Created:  2023-07-23T18:03:23.555Z
Modified: 2023-07-23T18:03:49.752Z
"""
from db import db

class UnidadMedica:
    @staticmethod
    def get_all():
        sql_query = "SELECT * FROM unidadesmd"
        result = db.session.execute(sql_query)
        unidadesmd = result.fetchall()
        return unidadesmd

    @staticmethod
    def get_by_id(idudm):
        sql_query = "SELECT * FROM unidadesmd WHERE idudm = :idudm"
        result = db.session.execute(sql_query, {'idudm': idudm})
        unidadmd = result.fetchone()
        return unidadmd

    def __init__(self, uni_codigo, cod_um_as400, cod_esigef, cod_crp, nombre_unidad, nom_corto_unidad,
                 nivel_atencion, tipologia_homo, complejidad, categ_establecimiento, coord_provincial, provincia,
                 cod_prov, canton, cod_cant, parroquia, cod_parroquia, zona, distrito):
        self.idudm = None
        self.uni_codigo = uni_codigo
        self.cod_um_as400 = cod_um_as400
        self.cod_esigef = cod_esigef
        self.cod_crp = cod_crp
        self.nombre_unidad = nombre_unidad
        self.nom_corto_unidad = nom_corto_unidad
        self.nivel_atencion = nivel_atencion
        self.tipologia_homo = tipologia_homo
        self.complejidad = complejidad
        self.categ_establecimiento = categ_establecimiento
        self.coord_provincial = coord_provincial
        self.provincia = provincia
        self.cod_prov = cod_prov
        self.canton = canton
        self.cod_cant = cod_cant
        self.parroquia = parroquia
        self.cod_parroquia = cod_parroquia
        self.zona = zona
        self.distrito = distrito