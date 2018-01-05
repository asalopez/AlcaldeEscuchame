#encoding:utf-8
"""
Definition of forms.
"""

from django import forms
from categorias.models import Categoria
from django.core.validators import RegexValidator

class QuejaForm(forms.Form):

    categoria = forms.ModelChoiceField(queryset = Categoria.objects.all(), empty_label = None);
    titulo = forms.CharField(max_length = 80, label = 'Título')
    cuerpo = forms.CharField(widget = forms.Textarea, label = 'Contenido')

    # Validaciones propias
    #def clean(self):
    #    password = self.cleaned_data["password"]
    #    confirm_password = self.cleaned_data["confirm_password"]
        
    #    if (password != confirm_password):
    #        raise forms.ValidationError("Por favor, asegúrese de confirmar correctamente su contraseña.")
