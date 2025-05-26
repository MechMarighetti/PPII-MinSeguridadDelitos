from django import forms
from apps.denuncia.models import Denuncia

class DenunciaForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        fields = ['delito', 'expediente', 'fecha_ocurrencia', 'descripcion', 'comisaria', 'fecha_registro']
        widgets = {
            'fecha_ocurrencia': forms.DateInput(
                attrs={
                    'type': 'date',
                    'placeholder': 'YYYY-MM-DD',
                    'class': 'form-control'
                },
                format='%Y-%m-%d'
            ),
            'fecha_registro': forms.DateInput(
                attrs={
                    'type': 'date',
                    'placeholder': 'YYYY-MM-DD',
                    'class': 'form-control'
                },
                format='%Y-%m-%d'
            ),
        }            