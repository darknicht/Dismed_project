from flask import render_template, request, flash, redirect, url_for
from models.unidadesmd_model import UnidadMedica
from db import db

def mostrar_unidadesmd():
    unidadesmd = UnidadMedica.get_all()
    return render_template('unidadesmd.html', unidadesmd=unidadesmd)

def mostrar_unidadmd(idudm):
    unidadmd = UnidadMedica.get_by_id(idudm)
    if unidadmd:
        return render_template('unidadmd.html', unidadmd=unidadmd)
    else:
        flash('Unidad médica no encontrada.', 'danger')
        return redirect(url_for('mostrar_unidadesmd'))

def editar_unidadmd_view(idudm):
    if request.method == 'POST':
        data = {
            'uni_codigo': request.form['uni_codigo'],
            'cod_um_as400': request.form['cod_um_as400'],
            'cod_esigef': request.form['cod_esigef'],
            'cod_crp': request.form['cod_crp'],
            'nombre_unidad': request.form['nombre_unidad'],
            'nom_corto_unidad': request.form['nom_corto_unidad'],
            'nivel_atencion': request.form['nivel_atencion'],
            'tipologia_homo': request.form['tipologia_homo'],
            'complejidad': request.form['complejidad'],
            'categ_establecimiento': request.form['categ_establecimiento'],
            'coord_provincial': request.form['coord_provincial'],
            'provincia': request.form['provincia'],
            'cod_prov': request.form['cod_prov'],
            'canton': request.form['canton'],
            'cod_cant': request.form['cod_cant'],
            'parroquia': request.form['parroquia'],
            'cod_parroquia': request.form['cod_parroquia'],
            'zona': request.form['zona'],
            'distrito': request.form['distrito']
        }
        
        if editar_unidadmd(idudm, data):
            flash('Unidad médica actualizada correctamente.', 'success')
        else:
            flash('Error al actualizar la unidad médica.', 'danger')
        
        return redirect(url_for('unidadesmd'))
    
    else:
        unidadmd = UnidadMedica.get_by_id(idudm)
        
        if unidadmd:
            return render_template('editar_unidadmd.html', unidadmd=unidadmd, editar_url=url_for('editar_unidadmd', idudm=idudm))
        else:
            flash('Unidad médica no encontrada.', 'danger')
            return redirect(url_for('mostrar_unidadesmd'))

def editar_unidadmd(idudm, data):
    sql_query = """
    UPDATE unidadesmd SET
        uni_codigo = :uni_codigo,
        cod_um_as400 = :cod_um_as400,
        cod_esigef = :cod_esigef,
        cod_crp = :cod_crp,
        nombre_unidad = :nombre_unidad,
        nom_corto_unidad = :nom_corto_unidad,
        nivel_atencion = :nivel_atencion,
        tipologia_homo = :tipologia_homo,
        complejidad = :complejidad,
        categ_establecimiento = :categ_establecimiento,
        coord_provincial = :coord_provincial,
        provincia = :provincia,
        cod_prov = :cod_prov,
        canton = :canton,
        cod_cant = :cod_cant,
        parroquia = :parroquia,
        cod_parroquia = :cod_parroquia,
        zona = :zona,
        distrito = :distrito
    WHERE idudm = :idudm
    """
    
    db.session.execute(sql_query, {
        'uni_codigo': data['uni_codigo'],
        'cod_um_as400': data['cod_um_as400'],
        'cod_esigef': data['cod_esigef'],
        'cod_crp': data['cod_crp'],
        'nombre_unidad': data['nombre_unidad'],
        'nom_corto_unidad': data['nom_corto_unidad'],
        'nivel_atencion': data['nivel_atencion'],
        'tipologia_homo': data['tipologia_homo'],
        'complejidad': data['complejidad'],
        'categ_establecimiento': data['categ_establecimiento'],
        'coord_provincial': data['coord_provincial'],
        'provincia': data['provincia'],
        'cod_prov': data['cod_prov'],
        'canton': data['canton'],
        'cod_cant': data['cod_cant'],
        'parroquia': data['parroquia'],
        'cod_parroquia': data['cod_parroquia'],
        'zona': data['zona'],
        'distrito': data['distrito'],
        'idudm': idudm
    })
    
    db.session.commit()
    return True

