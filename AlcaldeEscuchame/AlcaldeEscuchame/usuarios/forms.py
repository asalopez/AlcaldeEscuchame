#encoding:utf-8
"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class EditarPerfilForm(forms.Form):
    """ Formulario de edición """
    # Campos editables del User model
    email = forms.EmailField()
    first_name = forms.CharField(min_length = 2, max_length = 32, label = 'Nombre')
    last_name = forms.CharField(min_length = 2, max_length = 50, label = 'Apellidos')

    # Campos editables del Actor model
    poblacion = forms.CharField(max_length = 30, label = 'Población')
    telefono = forms.CharField(max_length = 9, label = 'Teléfono', required = False, validators = [RegexValidator(regex = r'^(6|9)(\d{8})$')])
    direccion = forms.CharField(max_length = 50, label = 'Dirección', required = False)
    foto = forms.URLField(required = False, label = 'Foto de perfil', validators = [RegexValidator(regex = r'((.png)|(.jpg)|(.jpge))$')])


class EditarClavesForm(forms.Form):
    """ Formulario de edición de las contraseñas de usuario """
    idUsuario = forms.IntegerField()
    actual_password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Contraseña actual')
    password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Nueva contraseña')
    confirm_password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Confirmar nueva contraseña')

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Valida la contraseña actual del usuario sea la que ha introducido en el formulario
            actual_password = self.cleaned_data["actual_password"]
            idUsuario = self.cleaned_data["idUsuario"]
            usuario = User.objects.get(pk = idUsuario)
            if not (usuario.check_password(actual_password)):
                    raise forms.ValidationError("Por favor, introduzca correctamente su contraseña actual para realizar el cambio.")

            # Valida que la nueva contraseña haya sido confirmada correctamente
            password = self.cleaned_data["password"]
            confirm_password = self.cleaned_data["confirm_password"]
            if (password != confirm_password):
                    raise forms.ValidationError("La nueva contraseña no coincide. Por favor, asegúrese de confirmarla correctamente.")