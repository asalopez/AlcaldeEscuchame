from django.db import models
from usuarios.models import Actor
from quejas.models import Queja

# Create your models here.
class Comentario(models.Model):
    fecha = models.DateTimeField(verbose_name = "Fecha de creación", auto_now = True);
    titulo = models.CharField(max_length = 80, help_text = 'Requerido. 80 carácteres como máximo.');
    cuerpo = models.TextField(max_length = 500, help_text = 'Requerido. 500 carácteres como máximo.');

    # Relaciones
    queja = models.ForeignKey(Queja, on_delete = models.CASCADE, null = True); # ManyToOne
    autor = models.ForeignKey(Actor, on_delete = models.CASCADE, null = True); # ManyToOne

    def __str__(self):
        return self.titulo + ' (' + str(self.fecha) + ')';