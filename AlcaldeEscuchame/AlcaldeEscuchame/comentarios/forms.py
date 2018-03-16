#encoding:utf-8
"""
Definition of forms.
"""

from django import forms
from django.core.validators import RegexValidator

class NuevoComentarioForm(forms.Form):
    """ Formulario para nuevo comentario """

    queja = forms.IntegerField();
    titulo = forms.CharField(max_length = 80, label = 'Título')
    cuerpo = forms.CharField(widget = forms.Textarea, label = 'Cuerpo')

