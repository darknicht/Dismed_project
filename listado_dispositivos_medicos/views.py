from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import ListadoDispositivosMedicos

@never_cache
@login_required
def listado_dispositivos_medicos_view(request):
    dispositivos = ListadoDispositivosMedicos.objects.all()
    return render(request, 'listado.html', {'dispositivos': dispositivos})
