from django.apps import AppConfig

class MatrizDispositivosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'matriz_dispositivos'

    def ready(self):
        import matriz_dispositivos.signals
