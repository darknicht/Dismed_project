from flask import render_template
from models.matrices_model import MatrizDispositivos, MatrizMedicamentos
from models.unidadesmd_model import UnidadMedica
from db import db

# Vista para mostrar la sección "VistaMatrices" con ambos listados
def mostrar_vista_matrices():
    # Recuperar datos de las matrices de dispositivos y medicamentos desde la base de datos
    matrices_dispositivos = MatrizDispositivos.get_all()
    matrices_medicamentos = MatrizMedicamentos.get_all()

    # Recuperar datos de unidad_medica desde la base de datos utilizando SQL manual
    unidades_medicas = UnidadMedica.get_all()

    # Crear un diccionario para mapear udm_id a la unidad médica correspondiente
    unidades_medicas_dict = {unidad.idudm: unidad.nombre_unidad for unidad in unidades_medicas}

    # Crear un diccionario para agrupar las matrices de dispositivos por udm_id
    matrices_dispositivos_dict = {}
    for matriz_dispositivo in matrices_dispositivos:
        nombre_unidad = matriz_dispositivo.nombre_unidad
        matriz_group = matrices_dispositivos_dict.setdefault(nombre_unidad, [])
        matriz_group.append(matriz_dispositivo)

    # Crear un diccionario para agrupar las matrices de medicamentos por nombre_unidad
    matrices_medicamentos_dict = {}
    for matriz_medicamento in matrices_medicamentos:
        nombre_unidad = matriz_medicamento.nombre_unidad
        matriz_group = matrices_medicamentos_dict.setdefault(nombre_unidad, [])
        matriz_group.append(matriz_medicamento)

    return render_template('vista_matrices.html', matrices_dispositivos=matrices_dispositivos_dict, matrices_medicamentos=matrices_medicamentos_dict, unidades_medicas=unidades_medicas_dict)

# Vista para mostrar una matriz de dispositivos específica
def mostrar_matriz_dispositivos(udm_id):
    matriz_dispositivos = MatrizDispositivos.get_by_id(udm_id)
    # Si tienes la implementación de get_unidad_medica_name() en el modelo MatrizDispositivos, puedes utilizarlo aquí
    nombre_unidad_medica = matriz_dispositivos.get_unidad_medica_name()
    return render_template('matriz_dispositivos.html', matriz_dispositivos=matriz_dispositivos, nombre_unidad_medica=nombre_unidad_medica)

# Vista para mostrar una matriz de medicamentos específica
def mostrar_matriz_medicamentos(idmatriz):
    matriz_medicamentos = MatrizMedicamentos.get_by_id(idmatriz)
    # Si tienes la implementación de get_unidad_medica_name() en el modelo MatrizMedicamentos, puedes utilizarlo aquí
    nombre_unidad_medica = matriz_medicamentos.get_unidad_medica_name()
    return render_template('matriz_medicamentos.html', matriz_medicamentos=matriz_medicamentos, nombre_unidad_medica=nombre_unidad_medica)


# Controlador para Matrices Dispositivos
def editar_matriz_dispositivos(idmatriz, data):
    # Consulta SQL para actualizar una matriz de dispositivos con el id proporcionado
    sql_query = """
    UPDATE matriz_dispositivos
    SET udm_id = :udm_id,
        version = :version,
        matrix = :matrix,
        item_nro = :item_nro,
        nom_subcomite = :nom_subcomite,
        nro_partida_pres = :nro_partida_pres,
        nom_partida_pres = :nom_partida_pres,
        cudim = :cudim,
        cod_iess = :cod_iess,
        cod_as400 = :cod_as400,
        nom_generico = :nom_generico,
        espec_tec = :espec_tec,
        pres_unimed = :pres_unimed,
        lvl_riesgo_suger = :lvl_riesgo_suger,
        lvl_aten_ia = :lvl_aten_ia,
        lvl_aten_ib = :lvl_aten_ib,
        lvl_aten_ic = :lvl_aten_ic,
        lvl_aten_ii = :lvl_aten_ii,
        lvl_aten_iii = :lvl_aten_iii,
        lvl_aten_aph = :lvl_aten_aph,
        espec_subespec = :espec_subespec,
        consumo_prom_proyec = :consumo_prom_proyec,
        perioci_consumo = :perioci_consumo,
        saldo_bodega_actual = :saldo_bodega_actual,
        proyecc_saldo = :proyecc_saldo,
        cant_pend_entre = :cant_pend_entre,
        cod_proceso = :cod_proceso,
        req_total_proyectado = :req_total_proyectado,
        stock_seguridad = :stock_seguridad,
        cant_program_inicial = :cant_program_inicial,
        cant_devol_prestam = :cant_devol_prestam,
        cant_final_required = :cant_final_required,
        prec_unit_ref = :prec_unit_ref,
        pres_ref_total = :pres_ref_total,
        dispo_dm = :dispo_dm,
        lvl_abastec = :lvl_abastec,
        tip_proc_cp = :tip_proc_cp,
        prim_cuatri_cant = :prim_cuatri_cant,
        prim_cuatri_mont = :prim_cuatri_mont,
        seg_cuatri_cant = :seg_cuatri_cant,
        seg_cuatri_mont = :seg_cuatri_mont,
        terc_cuatri_cant = :terc_cuatri_cant,
        terc_cuatri_mont = :terc_cuatri_mont,
        priorizacion = :priorizacion,
        observaciones = :observaciones,
        modify_time = CURRENT_TIMESTAMP,
        user_modify = :user_modify
    WHERE idmatriz = :idmatriz
    """

    # Ejecutar la consulta con los datos proporcionados
    db.session.execute(sql_query, {
        'udm_id': data['udm_id'],
        'version': data['version'],
        'matrix': data['matrix'],
        'item_nro': data['item_nro'],
        'nom_subcomite': data['nom_subcomite'],
        'nro_partida_pres': data['nro_partida_pres'],
        'nom_partida_pres': data['nom_partida_pres'],
        'cudim': data['cudim'],
        'cod_iess': data['cod_iess'],
        'cod_as400': data['cod_as400'],
        'nom_generico': data['nom_generico'],
        'espec_tec': data['espec_tec'],
        'pres_unimed': data['pres_unimed'],
        'lvl_riesgo_suger': data['lvl_riesgo_suger'],
        'lvl_aten_ia': data['lvl_aten_ia'],
        'lvl_aten_ib': data['lvl_aten_ib'],
        'lvl_aten_ic': data['lvl_aten_ic'],
        'lvl_aten_ii': data['lvl_aten_ii'],
        'lvl_aten_iii': data['lvl_aten_iii'],
        'lvl_aten_aph': data['lvl_aten_aph'],
        'espec_subespec': data['espec_subespec'],
        'consumo_prom_proyec': data['consumo_prom_proyec'],
        'perioci_consumo': data['perioci_consumo'],
        'saldo_bodega_actual': data['saldo_bodega_actual'],
        'proyecc_saldo': data['proyecc_saldo'],
        'cant_pend_entre': data['cant_pend_entre'],
        'cod_proceso': data['cod_proceso'],
        'req_total_proyectado': data['req_total_proyectado'],
        'stock_seguridad': data['stock_seguridad'],
        'cant_program_inicial': data['cant_program_inicial'],
        'cant_devol_prestam': data['cant_devol_prestam'],
        'cant_final_required': data['cant_final_required'],
        'prec_unit_ref': data['prec_unit_ref'],
        'pres_ref_total': data['pres_ref_total'],
        'dispo_dm': data['dispo_dm'],
        'lvl_abastec': data['lvl_abastec'],
        'tip_proc_cp': data['tip_proc_cp'],
        'prim_cuatri_cant': data['prim_cuatri_cant'],
        'prim_cuatri_mont': data['prim_cuatri_mont'],
        'seg_cuatri_cant': data['seg_cuatri_cant'],
        'seg_cuatri_mont': data['seg_cuatri_mont'],
        'terc_cuatri_cant': data['terc_cuatri_cant'],
        'terc_cuatri_mont': data['terc_cuatri_mont'],
        'priorizacion': data['priorizacion'],
        'observaciones': data['observaciones'],
        'user_modify': data['user_modify'],
        'idmatriz': idmatriz
    })

    # Confirmar los cambios en la base de datos
    db.session.commit()

# Controlador para Matrices Medicamentos
def editar_matriz_medicamentos(idmatriz, data):
    # Consulta SQL para actualizar una matriz de medicamentos con el id proporcionado
    sql_query = """
    UPDATE matriz_medicamentos
    SET udm_id = :udm_id,
        version = :version,
        matrix = :matrix,
        item_nro = :item_nro,
        nom_subcomite = :nom_subcomite,
        nro_partida_pres = :nro_partida_pres,
        nom_partida_pres = :nom_partida_pres,
        cod_cums = :cod_cums,
        principio_activo = :principio_activo,
        cod_cums_citox = :cod_cums_citox,
        desc_citox = :desc_citox,
        nom_generico = :nom_generico,
        atc_code = :atc_code,
        via_admon = :via_admon,
        forma_farm = :forma_farm,
        pres_unimed = :pres_unimed,
        consumo_prom_proyec = :consumo_prom_proyec,
        perioci_consumo = :perioci_consumo,
        saldo_bodega_actual = :saldo_bodega_actual,
        proyecc_saldo = :proyecc_saldo,
        cant_pend_entre = :cant_pend_entre,
        cod_proceso = :cod_proceso,
        req_total_proyectado = :req_total_proyectado,
        stock_seguridad = :stock_seguridad,
        cant_program_inicial = :cant_program_inicial,
        cant_devol_prestam = :cant_devol_prestam,
        cant_final_required = :cant_final_required,
        prec_unit_ref = :prec_unit_ref,
        pres_ref_total = :pres_ref_total,
        dispo_mm = :dispo_mm,
        lvl_abastec = :lvl_abastec,
        tip_proc_cp = :tip_proc_cp,
        prim_cuatri_cant = :prim_cuatri_cant,
        prim_cuatri_mont = :prim_cuatri_mont,
        seg_cuatri_cant = :seg_cuatri_cant,
        seg_cuatri_mont = :seg_cuatri_mont,
        terc_cuatri_cant = :terc_cuatri_cant,
        terc_cuatri_mont = :terc_cuatri_mont,
        priorizacion = :priorizacion,
        observaciones = :observaciones,
        modify_time = CURRENT_TIMESTAMP,
        user_modify = :user_modify
    WHERE idmatriz = :idmatriz
    """

    # Ejecutar la consulta con los datos proporcionados
    db.session.execute(sql_query, {
        'udm_id': data['udm_id'],
        'version': data['version'],
        'matrix': data['matrix'],
        'item_nro': data['item_nro'],
        'nom_subcomite': data['nom_subcomite'],
        'nro_partida_pres': data['nro_partida_pres'],
        'nom_partida_pres': data['nom_partida_pres'],
        'cod_cums': data['cod_cums'],
        'principio_activo': data['principio_activo'],
        'cod_cums_citox': data['cod_cums_citox'],
        'desc_citox': data['desc_citox'],
        'nom_generico': data['nom_generico'],
        'atc_code': data['atc_code'],
        'via_admon': data['via_admon'],
        'forma_farm': data['forma_farm'],
        'pres_unimed': data['pres_unimed'],
        'consumo_prom_proyec': data['consumo_prom_proyec'],
        'perioci_consumo': data['perioci_consumo'],
        'saldo_bodega_actual': data['saldo_bodega_actual'],
        'proyecc_saldo': data['proyecc_saldo'],
        'cant_pend_entre': data['cant_pend_entre'],
        'cod_proceso': data['cod_proceso'],
        'req_total_proyectado': data['req_total_proyectado'],
        'stock_seguridad': data['stock_seguridad'],
        'cant_program_inicial': data['cant_program_inicial'],
        'cant_devol_prestam': data['cant_devol_prestam'],
        'cant_final_required': data['cant_final_required'],
        'prec_unit_ref': data['prec_unit_ref'],
        'pres_ref_total': data['pres_ref_total'],
        'dispo_mm': data['dispo_mm'],
        'lvl_abastec': data['lvl_abastec'],
        'tip_proc_cp': data['tip_proc_cp'],
        'prim_cuatri_cant': data['prim_cuatri_cant'],
        'prim_cuatri_mont': data['prim_cuatri_mont'],
        'seg_cuatri_cant': data['seg_cuatri_cant'],
        'seg_cuatri_mont': data['seg_cuatri_mont'],
        'terc_cuatri_cant': data['terc_cuatri_cant'],
        'terc_cuatri_mont': data['terc_cuatri_mont'],
        'priorizacion': data['priorizacion'],
        'observaciones': data['observaciones'],
        'user_modify': data['user_modify'],
        'idmatriz': idmatriz
    })

    # Confirmar los cambios en la base de datos
    db.session.commit()
