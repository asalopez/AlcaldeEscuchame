#encoding:utf-8
"""
Definition of forms.
"""

from django import forms
from categorias.models import Categoria

class QuejaForm(forms.Form):

    categoria = forms.ModelChoiceField(queryset = Categoria.objects.all(), empty_label = None);
    titulo = forms.CharField(max_length = 80, label = 'Título')
    cuerpo = forms.CharField(widget = forms.Textarea, label = 'Contenido')
