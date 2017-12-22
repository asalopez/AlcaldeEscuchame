"""
Definition of forms.
"""
#encoding:utf-8

from django import forms
from django.core.validators import RegexValidator
from django.core import validators
from django.forms.models import ModelForm
from usuarios.models import Ciudadano
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Cuenta de usuario'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Contraseña'}))

class RegistroForm(forms.Form):
    # Campos requeridos por el User model
    username = forms.CharField(min_length = 5, max_length = 32)
    password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput)
    confirm_password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput)
    email = forms.EmailField()
    first_name = forms.CharField(min_length = 2, max_length = 32)
    last_name = forms.CharField(min_length = 2, max_length = 50)

    ## Campos requeridos por el Actor model
    poblacion = forms.CharField(max_length = 30)
    telefono = forms.CharField(max_length = 9, required = False, validators = [RegexValidator(regex = r'^(6|9)(\d{8})$')])
    direccion = forms.CharField(max_length = 50, required = False)
    foto = forms.URLField(required = False, validators = [RegexValidator(regex = r'((.png)|(.jpg)|(.jpge))$')])

    # Validaciones propias
    def clean(self):
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]
        
        if (password != confirm_password):
            raise forms.ValidationError("Por favor, asegúrese de confirmar correctamente su contraseña.")