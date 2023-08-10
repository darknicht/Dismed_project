from django.db import models
from django.contrib.auth.models import User

class RegistroImportacion(models.Model):
    fecha_importacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    archivo_importado = models.FileField(upload_to='importaciones/')  # Si quieres guardar el archivo importado
    version = models.IntegerField()  # La versión que se asignó durante esta importación

    def __str__(self):
        return f"Importación realizada el {self.fecha_importacion} por {self.usuario}"
