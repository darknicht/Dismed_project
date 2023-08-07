import secrets
from flask import Flask, render_template, flash, redirect, url_for
from dotenv import load_dotenv
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

# Carga de variables de entorno
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

# Manejo de errores
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error='Página no encontrada'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error='Error interno del servidor'), 500

if __name__ == '__main__':
    app.run(debug=True)
