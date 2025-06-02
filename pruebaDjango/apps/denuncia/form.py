from django import forms
from apps.denuncia.models import Denuncia
from django.contrib.auth.forms import AuthenticationForm

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
class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Usuario'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })     