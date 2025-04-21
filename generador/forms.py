from django import forms
from .models import Contrato

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['nombre', 'fecha_inicio', 'fecha_fin', 'requiere_aval', 'cuota_mantenimiento']