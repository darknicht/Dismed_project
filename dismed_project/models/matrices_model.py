"""
Author: Christian Aguirre (christian.david.aguirre@gmail.com)
matrices_model.py (c) 2023
Created:  2023-07-23T21:08:16.714Z
Modified: 2023-07-24T19:35:17.068Z
"""

from db import db

class MatrizDispositivos:
    @staticmethod
    def get_all():
        sql_query = """
            SELECT matriz_dispositivos.*, unidadesmd.nombre_unidad
            FROM matriz_dispositivos
            JOIN unidadesmd ON matriz_dispositivos.udm_id = unidadesmd.idudm
        """
        result = db.session.execute(sql_query)
        matriz_dispositivos = result.fetchall()
        return matriz_dispositivos
    
    @staticmethod
    def get_by_id(idmatriz):
        sql_query = "SELECT * FROM matriz_dispositivos WHERE idmatriz = :idmatriz"
        result = db.session.execute(sql_query, {'idmatriz': idmatriz})
        matriz_dispositivo = result.fetchall()
        return matriz_dispositivo

    @staticmethod
    def get_by_udm_id(udm_id):
        sql_query = "SELECT * FROM matriz_dispositivos WHERE udm_id = :udm_id"
        result = db.session.execute(sql_query, {'udm_id': udm_id})
        matrices_dispositivos = result.fetchall()
        return matrices_dispositivos

    # Puedes implementar otros métodos necesarios para esta clase...

class MatrizMedicamentos:
    @staticmethod
    def get_all():
        sql_query = """
            SELECT matriz_medicamentos.*, unidadesmd.nombre_unidad
            FROM matriz_medicamentos
            JOIN unidadesmd ON matriz_medicamentos.udm_id = unidadesmd.idudm
        """
        result = db.session.execute(sql_query)
        matriz_medicamentos = result.fetchall()
        return matriz_medicamentos
    
    @staticmethod
    def get_by_id(idmatriz_medicamento):
        sql_query = "SELECT * FROM matriz_medicamentos WHERE idmatriz_medicamento = :idmatriz_medicamento"
        result = db.session.execute(sql_query, {'idmatriz_medicamento': idmatriz_medicamento})
        matriz_medicamento = result.fetchone()
        return matriz_medicamento

    # Puedes implementar otros métodos necesarios para esta clase...