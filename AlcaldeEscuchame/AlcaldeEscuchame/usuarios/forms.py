#encoding:utf-8
"""
Definition of forms.
"""

from django import forms
from django.core.validators import RegexValidator

class EditarPerfilForm(forms.Form):
    # Campos editables del User model
    #password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput)
    #confirm_password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput)
    email = forms.EmailField()
    first_name = forms.CharField(min_length = 2, max_length = 32, label = 'Nombre')
    last_name = forms.CharField(min_length = 2, max_length = 50, label = 'Apellidos')

    ## Campos editables del Actor model
    poblacion = forms.CharField(max_length = 30, label = 'Población')
    telefono = forms.CharField(max_length = 9, label = 'Teléfono', required = False, validators = [RegexValidator(regex = r'^(6|9)(\d{8})$')])
    direccion = forms.CharField(max_length = 50, label = 'Dirección', required = False)
    foto = forms.URLField(required = False, validators = [RegexValidator(regex = r'((.png)|(.jpg)|(.jpge))$')])

    # Validaciones propias
    #def clean(self):
    #    password = self.cleaned_data["password"]
    #    confirm_password = self.cleaned_data["confirm_password"]
        
    #    if (password != confirm_password):
    #        raise forms.ValidationError("Por favor, asegúrese de confirmar correctamente su contraseña.")
