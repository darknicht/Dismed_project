from django import forms
from .models import UserProfile
from unidadesmd.models import UnidadMedica

class AssignUnitForm(forms.ModelForm):
    unidad_medica = forms.ModelChoiceField(
        queryset=UnidadMedica.objects.all(),
        required=False,
        label='Unidad Médica'
    )

    class Meta:
        model = UserProfile
        fields = ('unidad_medica',)
