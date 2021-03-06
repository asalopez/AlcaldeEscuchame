"""
Definition of forms.
"""
#encoding:utf-8

from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core import validators
from django.forms.models import ModelForm
from usuarios.models import Ciudadano
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class LoginForm(AuthenticationForm):
    """Formulario de inicio de sesión"""
    username = forms.CharField(max_length=254, widget=forms.TextInput({'class': 'form-control', 'required': True, 'autofocus': True, 'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(label=_("Contraseña"), widget=forms.PasswordInput({'class': 'form-control', 'required': True, 'placeholder':'Contraseña'}))


class RegistroForm(forms.Form):
    """Formulario registro"""

    # Campos requeridos por el User model
    username = forms.CharField(min_length = 5, max_length = 32, label = 'Nombre de usuario')
    password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Contraseña')
    confirm_password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Confirmar contraseña')
    email = forms.EmailField()
    first_name = forms.CharField(min_length = 2, max_length = 32, label = 'Nombre')
    last_name = forms.CharField(min_length = 2, max_length = 50, label = 'Apellidos')

    ## Campos requeridos por el Actor model
    poblacion = forms.CharField(max_length = 30, label = 'Población')
    telefono = forms.CharField(max_length = 9, required = False, validators = [RegexValidator(regex = r'^(6|9)(\d{8})$')], label = 'Teléfono')
    direccion = forms.CharField(max_length = 50, required = False, label = 'Dirección')
    foto = forms.URLField(required = False, validators = [RegexValidator(regex = r'((.png)|(.jpg)|(.jpge))$')], label = 'Foto de perfil')

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Valida que el username no sea repetido
            username = self.cleaned_data["username"]
            num_usuarios = User.objects.filter(username = username).count()
            if (num_usuarios > 0):
                    raise forms.ValidationError("El nombre de usuario ya está ocupado. Por favor, eliga otro para completar su registro.")

            # Valida que la contraseña se haya confirmado correctamente
            password = self.cleaned_data["password"]
            confirm_password = self.cleaned_data["confirm_password"]
            if (password != confirm_password):
                    raise forms.ValidationError("Las contraseñas introducidas no coinciden. Por favor, asegúrese de confirmarla correctamente.")

