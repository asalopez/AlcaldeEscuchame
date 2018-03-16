from django.db import models
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from usuarios.models import Actor
from quejas.models import Queja

class Comentario(models.Model):
    """
    Comentario: fecha, titulo, cuerpo, queja, autor
    """
    fecha = models.DateTimeField(verbose_name = "Fecha de creación", auto_now = True)
    titulo = models.CharField(max_length = 80, help_text = 'Requerido. 80 carácteres como máximo.')
    cuerpo = models.TextField(max_length = 500, help_text = 'Requerido. 500 carácteres como máximo.')

    # Relaciones
    queja = models.ForeignKey(Queja, on_delete = models.CASCADE, null = True); # ManyToOne
    autor = models.ForeignKey(Actor, on_delete = models.CASCADE, null = True); # ManyToOne

    def __str__(self):
        return self.titulo + ' (' + str(self.fecha) + ')'


class ComentarioAdminPanel(admin.ModelAdmin):
    """
    Clase que define los campos a mostrar en el Panel de Administración para el listado de Comentarios
    """
    list_display = ('titulo', 'queja', 'autor', 'fecha')