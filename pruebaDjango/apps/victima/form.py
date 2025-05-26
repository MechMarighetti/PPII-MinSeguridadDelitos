from django import forms
from apps.victima.models import Victima

class VictimaForm(forms.ModelForm):
    class Meta:
        model = Victima
        fields = ['genero', 'fecha_nacimiento', 'comuna_residencia']
        widgets = {
            'fecha_nacimiento': forms.DateInput(
                attrs={
                    'type': 'date',
                    'placeholder': 'YYYY-MM-DD',
                    'class': 'form-control'
                },
                format='%Y-%m-%d'
            ),
        }        