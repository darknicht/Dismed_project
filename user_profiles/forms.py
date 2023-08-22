from django import forms
from .models import UserProfile
from unidadesmd.models import UnidadMedica
from django.contrib.auth.models import User, Group

class SelectUserForm(forms.Form):
    selected_user_id = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name__in=['Operador 1', 'Operador 2', 'Operador 3']).order_by('username'),
        required=True,
        label='Seleccionar usuario',
    )

class AssignUnitForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name__in=['Operador 1', 'Operador 2', 'Operador 3']).order_by('username'),
        required=True,
        label='Usuario',
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=['Administrador', 'SuperAdmin', 'Operador 1', 'Operador 2', 'Operador 3']).order_by('name'),
        required=True,
        label='Grupo',
    )
    unidad_medica = forms.ModelChoiceField(
        queryset=UnidadMedica.objects.all().order_by('nombre_unidad'),
        required=False,
        label='Unidad Médica'
    )

    class Meta:
        model = UserProfile
        fields = ('user', 'unidad_medica',)
