from django import forms
from .models import Contrato

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = [
            'nombre',
            'empresa_cliente',
            'telefono_cliente',
            'email_cliente',
            'direccion_cliente',
            'descripcion',
            'dias_entrega',
            'meses_garantia',
            'vigencia_dias',
            'monto_total',
            'observaciones'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
            'monto_total': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'dias_entrega': forms.NumberInput(attrs={'min': '1', 'value': '30'}),
            'meses_garantia': forms.Select(),
            'vigencia_dias': forms.Select()
        }