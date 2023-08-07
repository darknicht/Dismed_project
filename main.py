import secrets
from flask import Flask, render_template, flash, redirect, url_for
from dotenv import load_dotenv
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

#Views
from views.matrices_view import mostrar_vista_matrices

#models
from models.matrices_model import MatrizDispositivos

# Carga de variables de entorno
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

# Matrices
@app.route('/matrices')
def vista_matrices():
    return mostrar_vista_matrices()

@app.route('/matrices/listado-matriz-dispositivos/<int:udm_id>')
def mostrar_matriz_dispositivos(udm_id):
    matrices_dispositivos = MatrizDispositivos.get_by_udm_id(udm_id)
    return render_template('listado_matriz_dispositivos.html', matrices_dispositivos=matrices_dispositivos)


@app.route('/matrices/listado-matriz-medicamentos/<int:udm_id>')
def mostrar_matriz_medicamentos(udm_id):
    # Recuperar los datos de la matriz de medicamentos por su id
    matriz_medicamento = MatrizMedicamentos.get_by_id(udm_id)
    return render_template('editar_matriz_medicamentos.html', matriz_medicamento=matriz_medicamento)

# Manejo de errores
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error='Página no encontrada'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error='Error interno del servidor'), 500

if __name__ == '__main__':
    app.run(debug=True)
