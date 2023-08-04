from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UnidadMedica
from django.urls import reverse

def mostrar_unidadesmd(request):
    unidadesmd = UnidadMedica.objects.all()
    return render(request, 'unidadesmd.html', {'unidadesmd': unidadesmd})

def mostrar_unidadmd(request, idudm):
    try:
        unidadmd = UnidadMedica.objects.get(pk=idudm)
        return render(request, 'unidadmd.html', {'unidadmd': unidadmd})
    except UnidadMedica.DoesNotExist:
        messages.error(request, 'Unidad médica no encontrada.')
        return redirect(reverse('mostrar_unidadesmd'))

def editar_unidadmd_view(request, idudm):
    try:
        unidadmd = UnidadMedica.objects.get(pk=idudm)
        if request.method == 'POST':
            # Actualizar datos de unidad médica
            for key, value in request.POST.items():
                if hasattr(unidadmd, key):
                    setattr(unidadmd, key, value)
            unidadmd.save()
            messages.success(request, 'Unidad médica actualizada correctamente.')
            return redirect(reverse('unidadesmd'))
        else:
            return render(request, 'editar_unidadmd.html', {'unidadmd': unidadmd, 'editar_url': reverse('editar_unidadmd', args=[idudm])})
    except UnidadMedica.DoesNotExist:
        messages.error(request, 'Unidad médica no encontrada.')
        return redirect(reverse('mostrar_unidadesmd'))
