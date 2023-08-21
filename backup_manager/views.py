# backup_manager/views.py

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from dotenv import load_dotenv
from datetime import datetime
import subprocess
import logging
import os

logger = logging.getLogger(__name__)

@user_passes_test(lambda u: u.is_superuser)
def crear_backup(request):
    if request.method == 'POST':
        # Cargar variables de entorno desde el archivo .env en dismed_project
        env_path = os.path.join(settings.BASE_DIR, './dismed_project/.env')

        load_dotenv(dotenv_path=env_path)
        db_user = os.getenv('DB_USER')
        db_name = os.getenv('DB_NAME')
        db_password = os.getenv('DB_PASSWORD')  # Obtener la contraseña desde el archivo .env
        if db_user is None or db_name is None or db_password is None:
            return HttpResponse('Error al cargar las variables de entorno.', status=500)
        
        backup_folder_path = os.path.join(settings.BASE_DIR, 'backup_manager/backups')
        os.makedirs(backup_folder_path, exist_ok=True)
        # Generar un nombre de archivo basado en la fecha y hora actual
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_file_name = f'backup_{timestamp}.snmd1'
        backup_file_path = os.path.join(backup_folder_path, backup_file_name)
        command = f"pg_dump -U {db_user} -F c -b -v -f {backup_file_path} {db_name}"
        env = os.environ.copy()
        env['PGPASSWORD'] = str(db_password)  # Establecer la variable de entorno PGPASSWORD

        try:
            result = subprocess.run(command, shell=True, check=True, stderr=subprocess.PIPE, env=env)
            return HttpResponse(f'Backup creado exitosamente en {backup_file_path}')
        except subprocess.CalledProcessError as e:
            logger.error(f"Raw error bytes: {e.stderr}")
            try:
                error_message = e.stderr.decode()
            except UnicodeDecodeError:
                error_message = "Error al decodificar el mensaje de error."
            return HttpResponse(f'Error al crear el backup: {error_message}', status=500)
    else:
        # Renderizar la plantilla HTML
        return render(request, 'backup.html')

