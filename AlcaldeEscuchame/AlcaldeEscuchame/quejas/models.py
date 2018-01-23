from django.db import models
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.core import validators
from django.core.validators import RegexValidator
from usuarios.models import Ciudadano
from django.core.validators import MinValueValidator, MaxValueValidator
from categorias.models import Categoria

# Queja: referencia, fecha, titulo, cuerpo, estado (Abierta ó Tramitada)
class Queja(models.Model):
    # Posibles estados de una queja
    ABIERTA = 'Abierta'
    TRAMITADA = 'Tramitada'
    ESTADOS_QUEJA = (
        (ABIERTA, 'Abierta'),
        (TRAMITADA, 'Tramitada')
    )

    # Model fields
    referencia = models.CharField(max_length = 7, unique = True, validators = [RegexValidator(regex = r'^([a-zA-Z]{2})-([a-zA-Z0-9]{4})$', message = 'La referencia no cumple el patrón solicitado.')],
                                  help_text = 'Requerido. 7 carácteres que cumplan el patrón: dos letras, un guión y cuatro caracteres (letras o dígitos). Ejemplo: QU-1aZ9')
    fecha = models.DateTimeField(verbose_name = "Fecha de publicación/actualización", auto_now = True)
    titulo = models.CharField(max_length = 100)
    cuerpo = models.TextField(max_length = 5000)
    estado = models.CharField(max_length = 10, choices = ESTADOS_QUEJA, default = ABIERTA)

    # Relaciones
    votantes = models.ManyToManyField(Ciudadano, through = 'Valoracion', related_name = 'votantes',
                                      through_fields=('queja', 'ciudadano'))
    categoriaManual = models.ForeignKey(Categoria, null = True, verbose_name = 'Categorización Manual')
        # Hacemos la categorización unidireccional (related_name = '+')
    categoriaAutomatica = models.ForeignKey(Categoria, related_name = '+', null = True, verbose_name = 'Categorización Automática')
    ciudadano = models.ForeignKey(Ciudadano, on_delete = models.CASCADE, null = True)

    def __str__(self):
        return self.titulo + ' (' + self.referencia + ')'


# Clase que define los campos a mostrar en el Panel de Administración para el listado de quejas
class QuejaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoriaManual', 'ciudadano', 'categoriaAutomatica', 'estado', 'fecha')


# Valoración: puntos, ciudadano, queja.
class Valoracion(models.Model):
    puntuacion = models.IntegerField(validators = [MaxValueValidator(5), MinValueValidator(1)], help_text = 'Requerido. Rango de 1 a 5 (inclusives).')

    # Relaciones
    ciudadano = models.ForeignKey(Ciudadano, on_delete = models.CASCADE, null = True)
    queja = models.ForeignKey(Queja, on_delete = models.CASCADE, null = True)

    def __str__(self):
        return str(self.ciudadano) + 'valora la queja ' + self.queja.referencia +' - ' + str(self.puntuacion) + ' puntos.'

    class Meta:
        verbose_name_plural = "Valoraciones"
        unique_together = ('ciudadano', 'queja')


# Clase que define los campos a mostrar en el Panel de Administración para el listado de valoraciones
class ValoracionAdmin(admin.ModelAdmin):
    list_display = ('puntuacion', 'ciudadano', 'queja')
