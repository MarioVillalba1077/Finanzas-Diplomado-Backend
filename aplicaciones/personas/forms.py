from django import forms
from .models import Persona

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        # fields = ['nombre', 'apellido', 'tipo_documento', 'numero_documento', 'direccion', 'ciudad', 'celular', 'email', 'estado']
        fields = ['nombre', 'apellido', 'tipo_documento', 'numero_documento', 'direccion', 'celular', 'email', 'estado']
