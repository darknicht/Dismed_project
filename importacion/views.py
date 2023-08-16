from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd
from matriz_dispositivos.models import MatrizDispositivos
from unidadesmd.models import UnidadMedica
from importacion.models import RegistroImportacion

def validate_and_clean_data(data):
    # Limpia y valida el campo 'cant_pend_entre'
    data['cant_pend_entre'].fillna(0, inplace=True)

    # Lista de campos específicos para reemplazar NaN por un guión
    campos = ['cod_proceso', 'cudim', 'lvl_aten_ia', 'lvl_aten_ib', 'lvl_aten_ic', 'lvl_aten_ii', 'lvl_aten_iii', 'lvl_aten_aph', 'observaciones']

    # Reemplaza NaN en los campos específicos por un guión
    for campo in campos:
        data[campo].fillna('-', inplace=True)

    # Aquí añadir más validaciones y limpiezas según sea necesario
    return data

def upload_matriz(request):
    if request.method == 'POST':
        messages.info(request, "Archivo recibido")
        excel_file = request.FILES["excel_file"]
        unidad_medica_selected = request.POST.get('unidad_medica')

        try:
            unidad = UnidadMedica.objects.get(pk=unidad_medica_selected)

            # Buscar la última versión en la base de datos para esa unidad médica y incrementarla en 1
            last_version = MatrizDispositivos.objects.filter(unidad_medica=unidad).order_by('-version').first()
            new_version = last_version.version + 1 if last_version else 1

            data = pd.read_excel(excel_file)
            data = validate_and_clean_data(data)
            for _, row in data.iterrows():
                matriz = MatrizDispositivos()
                matriz.unidad_medica = unidad
                matriz.version = new_version
                matriz.item_nro = row['item_nro']
                matriz.nom_subcomite = row['nom_subcomite']
                matriz.nro_partida_pres = row['nro_partida_pres']
                matriz.nom_partida_pres = row['nom_partida_pres']
                matriz.cudim = row['cudim']
                matriz.cod_iess = row['cod_iess']
                matriz.cod_as400 = row['cod_as400']
                matriz.nom_generico = row['nom_generico']
                matriz.espec_tec = row['espec_tec']
                matriz.pres_unimed = row['pres_unimed']
                matriz.lvl_riesgo_suger = row['lvl_riesgo_suger']
                matriz.lvl_aten_ia = row['lvl_aten_ia']
                matriz.lvl_aten_ib = row['lvl_aten_ib']
                matriz.lvl_aten_ic = row['lvl_aten_ic']
                matriz.lvl_aten_ii = row['lvl_aten_ii']
                matriz.lvl_aten_iii = row['lvl_aten_iii']
                matriz.lvl_aten_aph = row['lvl_aten_aph']
                matriz.espec_subespec = row['espec_subespec']
                matriz.consumo_prom_proyec = row['consumo_prom_proyec']
                matriz.perioci_consumo = row['perioci_consumo']
                matriz.saldo_bodega_actual = row['saldo_bodega_actual']
                matriz.proyecc_saldo = row['proyecc_saldo']
                matriz.cant_pend_entre = row['cant_pend_entre']
                matriz.cod_proceso = row['cod_proceso']
                matriz.req_total_proyectado = row['req_total_proyectado']
                matriz.stock_seguridad = row['stock_seguridad']
                matriz.cant_program_inicial = row['cant_program_inicial']
                matriz.cant_devol_prestam = row['cant_devol_prestam']
                matriz.cant_final_required = row['cant_final_required']
                matriz.prec_unit_ref = row['prec_unit_ref']
                matriz.pres_ref_total = row['pres_ref_total']
                matriz.dispo_dm = row['dispo_dm']
                matriz.lvl_abastec = row['lvl_abastec']
                matriz.tip_proc_cp = row['tip_proc_cp']
                matriz.prim_cuatri_cant = row['prim_cuatri_cant']
                matriz.prim_cuatri_mont = row['prim_cuatri_mont']
                matriz.seg_cuatri_cant = row['seg_cuatri_cant']
                matriz.seg_cuatri_mont = row['seg_cuatri_mont']
                matriz.terc_cuatri_cant = row['terc_cuatri_cant']
                matriz.terc_cuatri_mont = row['terc_cuatri_mont']
                priorizacion_value = True if row['priorizacion'] == 'SI' else False
                matriz.priorizacion = priorizacion_value
                matriz.observaciones = row['observaciones']
                matriz.user_modify = request.user.username
                matriz.user_create = request.user.username

                # Antes de guardar, verificamos si el registro ya existe
                exists = MatrizDispositivos.objects.filter(
                    cod_as400=row['cod_as400'], 
                    unidad_medica=unidad,
                    version=new_version
                ).exists()

                if not exists:
                    matriz.save()
                else:
                    messages.warning(request, f'El registro con cod_as400 {row["cod_as400"]} ya existe para esa combinación y no fue importado.')

            # Crear un registro en RegistroImportacion
            registro = RegistroImportacion(
                usuario=request.user,
                archivo_importado=excel_file,  # Esta línea se encarga de guardar el archivo con el nombre personalizado
                version=new_version,
                unidad_medica=unidad
            )
            registro.save()

            messages.success(request, 'Datos importados exitosamente!')
        except Exception as e:
            print(e)
            messages.error(request, f'Error al importar: {e}')

        return redirect('/importacion/upload/')

    unidades_medicas = UnidadMedica.objects.all()
    return render(request, 'upload_matriz.html', {'unidades_medicas': unidades_medicas})

def registros_importacion(request):
    registros = RegistroImportacion.objects.all().order_by('-fecha_importacion')  # Obtener registros ordenados por fecha descendente
    return render(request, 'registro_importaciones.html', {'registros': registros})