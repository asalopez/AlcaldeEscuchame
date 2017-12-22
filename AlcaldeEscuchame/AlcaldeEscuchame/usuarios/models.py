from django.db import models
from django.core.validators import RegexValidator
from django.core import validators
from categorias.models import Categoria

# Create your models here.
class Actor(models.Model):
    poblacion = models.CharField(max_length = 30, help_text = 'Requerido. 30 carácteres como máximo.')
    telefono = models.CharField(max_length = 9, null = True, blank = True, help_text = 'Opcional. 9 dígitos como máximo. Debe comenzar por 6 ó 9.',
                                validators = [RegexValidator(regex = r'^(6|9)(\d{8})$', message = 'El teléfono no cumple con el patrón solicitado.')])
    direccion = models.CharField(max_length = 50, null = True, blank = True, help_text = 'Opcional. 50 carácteres como máximo.')
    foto = models.URLField(verbose_name = 'Imagen de perfil', name = 'imagen', null = True, blank = True, help_text = 'Opcional. URL a la imagen en formato PNG, JPG o JPGE.',
                           validators = [RegexValidator(regex = r'((.png)|(.jpg)|(.jpge))$', message = 'La URL no corresponde con una imagen en formato especificado.')])

class Ciudadano(Actor):
    usuario = models.OneToOneField('auth.User', unique = True, null = True)
    
    def __str__(self):
        return self.usuario.get_full_name() + ' (' + self.usuario.get_username() + ')'


class Funcionario(Actor):
    usuario = models.OneToOneField('auth.User', unique = True, null = True)

    # Relaciones
    categorias = models.ManyToManyField(Categoria)

    def __str__(self):
        return self.usuario.get_full_name() + ' (' + self.usuario.get_username() + ')'

class Administrador(Actor):
    usuario = models.OneToOneField('auth.User', unique = True, null = True)

    def __str__(self):
        return self.usuario.get_full_name() + ' (' + self.usuario.get_username() + ')'

    class Meta:
        verbose_name_plural = "Administradores"