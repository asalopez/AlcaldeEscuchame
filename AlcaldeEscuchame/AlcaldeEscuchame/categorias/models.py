from django.db import models
from django.core import validators
from django.core.validators import RegexValidator

# Categoría: imagen, nombre y descripción
class Categoria(models.Model):
    imagen =  models.URLField(verbose_name = 'Imagen de perfil', null = True, blank = True, help_text = 'Opcional. URL a la imagen en formato PNG, JPG o JPGE.',
                           validators = [RegexValidator(regex = r'((.png)|(.jpg)|(.jpge))$', message = 'La URL no corresponde con una imagen en formato especificado.')]);
    nombre = models.CharField(max_length = 80, help_text = 'Requerido. 80 carácteres como máximo.');
    descripcion = models.TextField(max_length = 300, help_text = 'Requerido. 300 carácteres como máximo.');

    def __str__(self):
        return self.nombre;

