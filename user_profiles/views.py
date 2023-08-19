from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AssignUnitForm

@login_required
def assign_unit_view(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = AssignUnitForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Unidad médica asignada con éxito.')
            return redirect('profile_view') # Redirige a la vista del perfil o cualquier otra vista que desees.
    else:
        form = AssignUnitForm(instance=profile)

    return render(request, 'assign_unit.html', {'form': form})
